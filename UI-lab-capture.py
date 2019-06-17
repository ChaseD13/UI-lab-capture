import u3 
import LabJackPython
import time
import tkinter as tk
import datetime  #now.strftime("%Y-%m-%d %H:%M")
import matplotlib.figure as figure
import matplotlib.animation as animation
import matplotlib.pylab as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import PySpin
import os
try:
    import Queue
except ImportError:  # Python 3
    import queue as Queue
from copy import deepcopy
import sys
import traceback
from PIL import Image, ImageTk
import signal
import threading
import gc


# Add funtions purpose here....
# Properties: now, ad_var
# Functions: prompt_window, update_window, submit_ad
# Explanantion: Active directory is used as a term to describe the directory set by the user where they want to save various files
# References: "Settings window", 
class SettingsWindow():
    def __init__(self):
        self.now = datetime.datetime.now()
        
    def prompt_window(self):
        #Initialize a window
        self.root = tk.Tk()

        #Change the title of the window
        self.root.title("Active Directory and Other Settings")

        #width x height + x_offset + y_offset:
        self.root.geometry("1000x1000+0+0")
        self.root.state('zoomed')

        #Variables
        self.ad_var = tk.StringVar() #Holds the active directory string.

        self.wd_var = tk.StringVar() #Holds the date string

        self.basefile_var = tk.StringVar() #Holds the Vole number. Assigned by the user.

        self.pcamera_var = tk.IntVar() #Holds the serial number for the primary labjack camera
        self.pcamera_var.set(19061331)

        self.splitsize_var = tk.IntVar()


        #Labels for entry boxes
        tk.Label(self.root, text = "Working Directory: ",).grid(row = 0, column = 0, padx = 10, pady = 10)
        tk.Label(self.root, text = "Base File Name: ").grid(row = 1, column = 0, padx = 10, pady = 10)
        tk.Label(self.root, text = "Active Directory: ").grid(row = 2, column = 0, padx = 10, pady = 10)
        tk.Label(self. root, text = "Primary Camera Serial Number: ").grid(row = 3, column = 0, padx = 10, pady = 10) 
        tk.Label(self.root, text = "File Split Size: ").grid(row = 4, column = 0, padx = 10, pady = 10)


        #Entry boxes
        self.wd_slot = tk.Entry(self.root, textvariable = self.wd_var, justify = "left", width = 80) #Entry variable for setting the date.
        self.wd_slot.grid(row = 0, column = 2, padx = 10, pady = 10)

        self.basefile_slot = tk.Entry(self.root, textvariable = self.basefile_var, justify = "left", width = 80) #Entry variable for setting the vole number. 
        self.basefile_slot.grid(row = 1, column = 2, padx = 10, pady = 10)

        self.ad_slot = tk.Entry(self.root, textvariable = self.ad_var, justify = "left", width = 80) #Entry variable that displays the current AD as it is being filled in.
        self.ad_slot.grid(row = 2, column = 2, padx = 10, pady = 10)

        self.primary_slot = tk.Entry(self.root, textvariable = self.pcamera_var, justify = "left", width = 80) #Entry variable for setting the primary camera's serial number 
        self.primary_slot.grid(row = 3, column = 2, padx = 10, pady = 10)

        self.splitsize_slot = tk.Entry(self.root, textvariable = self.splitsize_var, justify = "left", width = 80) #Entry variable for setting the primary camera's serial number 
        self.splitsize_slot.grid(row = 4, column = 2, padx = 10, pady = 10)

        tk.Button(self.root, text = "Submit", command = self.submit_ad).grid(row = 5, column = 0, padx = 20, pady = 10) #Button that when pressed closes the settings window

        #Function Calls

        self.update_window() #Call to update the window when the user types in new values into the entry fields.

        #Start the window
        self.root.mainloop() 

    #Function that updates 
    def update_window(self):
        self.ad_var.set(self.wd_var.get() + "/" + self.basefile_var.get() + ".txt")
        self.after_event = self.root.after(5, self.update_window)
        self.root.update()

    #Function to close the window and confirm the active directory being used by the user 
    def submit_ad(self):
        self.root.after_cancel(self.after_event)
        self.root.destroy()
    
    
# Add funtions purpose here....
# Properties: None
# Functions: init_labjack, update_voltage, build_window, animate
class UILabCapture():
    # Initialization; Takes in an active directory path as a parameter
    def __init__(self, active_directory, primary_serial_number, fss):
        self.filepath = active_directory # Active directory path is stored in a local varaible
        self.primary_sn = primary_serial_number # The serial number of the primary Blackfly S camera
        self.fileSplitSize = fss # The size of the file split
        self.image_queue_primary = Queue.Queue() # Shared queue between threads to save and record frames from the primary camera
        self.image_queue_secondary = Queue.Queue() # Shared queue between threads to save and record frames from the secondary camera
        self.running_experiment = False # Boolean value to keep track wther or not there is an experiment running currently
        self.missed_frames_p = 0 # (Primary) Counter for the number of missed frames during the stream
        self.prev_frame_id_p = -1 # (Primary) Holds the previous FrameID; -1 b/c FrameID's begin @ 0
        self.missed_frames_s = 0 # (Secondary) Counter for the number of missed frames during the stream
        self.prev_frame_id_s = -1 # (Secondary) Holds the previous FrameID; -1 b/c FrameID's begin @ 0
 
    # Builds the main GUI window 
    def build_window(self):
        # Initialize a window
        self.root = tk.Tk()
        
        self.camera_frame = tk.Frame(self.root)
        self.camera_frame.pack(side = "top", fill = "x")
        # self.camera_frame.grid_rowconfigure(1, weight = 1)
        # self.camera_frame.grid_columnconfigure(3, weight = 1)

        self.labjack_values = tk.Frame(self.root)
        self.labjack_values.pack(side = "left", expand = True, fill = "both")
        # self.labjack_values.grid_rowconfigure(0, weight = 1)
        # self.labjack_values.grid_columnconfigure(0, weight = 1)

        self.scrolling_graph = tk.Frame(self.root)
        self.scrolling_graph.pack(side = "right", expand = True, fill = "both")
        # self.scrolling_graph.grid_rowconfigure(0, weight = 1)
        # self.scrolling_graph.grid_columnconfigure(0, weight = 1)


        # Style

        # Change the title of the window
        self.root.title("UI Lab Capture")
        # width x height + x_offset + y_offset:
        self.root.geometry("1000x1000+0+0") 
        self.root.state('zoomed')


        # Variables

        self.var0 = tk.IntVar() # Voltage being read from the labjack at FIO0
        self.var1 = tk.IntVar() # Voltage being read from the labjack at FIO1
        self.var2 = tk.IntVar() # Voltage being read from the labjack at FIO2
        self.var3 = tk.IntVar() # Voltage being read from the labjack at FIO3
        self.var4 = tk.IntVar() # Voltage being read from the labjack at FIO4
        self.var5 = tk.IntVar() # Voltage being read from the labjack at FIO5
        self.var6 = tk.IntVar() # Voltage being read from the labjack at FIO6
        self.var7 = tk.IntVar() # Voltage being read from the labjack at FIO7


        #Labels

        # Label that is filling the space where the camera will be
        self.cameras = tk.Label(self.camera_frame, text = "Space for Cameras", bg = "orange", height = 20)
        self.cameras.pack(fill = "both")

        # Labels for the FIO 0-7 ports on the labjacks
        tk.Label(self.labjack_values, text = "AIN0: ").pack()
        self.ain_zero = tk.Label(self.labjack_values, textvariable = self.var0)
        self.ain_zero.pack()

        tk.Label(self.labjack_values, text = "AIN1: ").pack()
        self.ain_one = tk.Label(self.labjack_values, textvariable = self.var1)
        self.ain_one.pack()

        tk.Label(self.labjack_values, text = "AIN2: ").pack()
        self.ain_two = tk.Label(self.labjack_values, textvariable = self.var2)
        self.ain_two.pack()

        tk.Label(self.labjack_values, text = "AIN3: ").pack()
        self.ain_three = tk.Label(self.labjack_values, textvariable = self.var3)
        self.ain_three.pack()

        tk.Label(self.labjack_values, text = "AIN4: ").pack()
        self.ain_four = tk.Label(self.labjack_values, textvariable = self.var4)
        self.ain_four.pack()

        tk.Label(self.labjack_values, text = "AIN5: ").pack()
        self.ain_five = tk.Label(self.labjack_values, textvariable = self.var5)
        self.ain_five.pack()

        tk.Label(self.labjack_values, text = "AIN6: ").pack()
        self.ain_six = tk.Label(self.labjack_values, textvariable = self.var6)
        self.ain_six.pack()

        tk.Label(self.labjack_values, text = "AIN7: ").pack()
        self.ain_seven = tk.Label(self.labjack_values, textvariable = self.var7)
        self.ain_seven.pack()



        # Scales
        # Scale for users to adjust the scan speed in Hz
        # self.scan_scale = tk.Scale(self.labjack_values, from_=0.1, to=100, orient = tk.HORIZONTAL, label = "Scan rate (Hz)", length = 500, resolution = 1)
        # self.scan_scale.grid(row = 3, column = 0, columnspan = 8)
        # self.scan_scale.set(1)


        self.scan_hz = tk.IntVar()
        self.scan_hz.set("Enter desired hz...")
        self.scan_space = tk.Entry(self.labjack_values, textvariable = self.scan_hz)
        self.scan_space.pack(padx = 10, pady = 10)

        # Input for the number of channels
        # self.num_channels = tk.IntVar()
        # self.num_channels.set("# of channels...")
        # self.num_channels_entry = tk.Entry(self.labjack_values, textvariable = self.num_channels)
        # self.num_channels_entry.pack(padx = 10, pady = 10)

        # Button
        tk.Button(self.labjack_values, text = "Start Experiment", command = self.start_gui).pack(padx = 10, pady = 10)
        tk.Button(self.labjack_values, text = "Stop Experiment", command = self.stop_gui).pack(padx = 10, pady = 10)


        self.f = figure.Figure(figsize = (5,4))

        # Create a cnvas in the window to place the figure into 
        self.canvas = FigureCanvasTkAgg(self.f, self.scrolling_graph)
        self.canvas.get_tk_widget().pack(side = "top", fill = "both", expand = True)
        self.canvas.draw()

        #Frame to hold camera images

        #Handle interrupt 
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Start the window
        self.root.mainloop() 


    # Function to initialize the lab jack, get its configuration data, and set the FIO ports to analog.
    # try/except case is used to check if the labjack is able to be opened, if not a statement is preinted and the function closes the labjack 
    def init_labjack(self):
        try:
            self.d = u3.U3() # Connect to labjack 
            self.d.getCalibrationData() # Calibration data will be used by functions that convert binary data to voltage/temperature and vice versa
            self.d.configIO(FIOAnalog= 255) # Set the FIO to read in analog; 255 sets all eight FIO ports to analog
            #self.d.streamConfig(NumChannels= self.num_channels.get(), PChannels=range(self.num_channels.get()), NChannels=[31]*self.num_channels.get(), Resolution=1, ScanFrequency=self.scan_hz.get())
            self.d.streamConfig(NumChannels= 8, PChannels=range(8), NChannels=[31]*8, Resolution=1, ScanFrequency=self.scan_hz.get())
            
        except:
            LabJackPython.Close() #Close all UD driver opened devices in the process


    # Update voltage is used to constantly monitor the AIN0 port to see what voltage the port is reciving
    # It is adjusted by the scan_scale variable to scan faster or slower
    def update_voltage(self):
        # Try to set the update interval equal to the desired Hz converted into milliseconds
        # try:
        #     self.update_interval =int((1/self.scan_scale.get())*1000)
        # except:
        #     pass
        try:
            self.var0.set(round(self.d.getAIN(0), 3)) # Get and set voltage for port 0
            self.var1.set(round(self.d.getAIN(1), 3)) # Get and set voltage for port 1
            self.var2.set(round(self.d.getAIN(2), 3)) # Get and set voltage for port 2
            self.var3.set(round(self.d.getAIN(3), 3)) # Get and set voltage for port 3
            self.var4.set(round(self.d.getAIN(4), 3)) # Get and set voltage for port 4
            self.var5.set(round(self.d.getAIN(5), 3)) # Get and set voltage for port 5
            self.var6.set(round(self.d.getAIN(6), 3)) # Get and set voltage for port 6
            self.var7.set(round(self.d.getAIN(7), 3)) # Get and set voltage for port 7
        except: 
            self.d.streamStop()
            self.update_voltage()

        # self.ani = animation.FuncAnimation(self.fig, self.animate, fargs=self.fargs, interval=self.update_interval)

        #self.root.update() #Update the window
        #self.root.after(self.update_interval, self.update_voltage) #Schedule for this function to call itself agin after update_interval milliseconds


    # Function to wrtie the data out to a directory
    # TODO: Find what data needs to be written out to the directory 
    def write_to_file(self):
        try:
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            with open(self.filepath, "w") as f:
                f.write("This is test data \n")
        finally:
            f.close()


    # Handles the setup and initialization of both cameras and the avi video
    # TODO: Add trigger functionality to align captured frames
    def operate_cameras(self):
        # Get system
        self.system = PySpin.System.GetInstance()
        # Get camera list
        self.cam_list = self.system.GetCameras()
        # Figure out which is primary and secondary
        if self.cam_list.GetByIndex(0).TLDevice.DeviceSerialNumber() == str(self.primary_sn):
            self.cam_primary = self.cam_list.GetByIndex(0)
            self.cam_secondary = self.cam_list.GetByIndex(1)
        else:
            self.cam_primary = self.cam_list.GetByIndex(1)
            self.cam_secondary = self.cam_list.GetByIndex(0)
 
        # Initialize cameras
        self.cam_primary.Init()
        self.cam_secondary.Init()

        # Retrieve GenICam nodemap
        self.primary_nodemap = self.cam_primary.GetNodeMap()
        self.secondary_nodemap = self.cam_secondary.GetNodeMap()

        # Retrieve nodemap TLDevice
        self.primary_nodemaptldevice = self.cam_primary.GetTLDeviceNodeMap()
        self.secondary_nodemaptldevice = self.cam_secondary.GetTLDeviceNodeMap()

        # Setup the hardware triggers
        # NOTE: Turned off for now because gpio pins not connected

        # # Set up primary camera trigger
        # self.cam_primary.LineSelector.SetValue(PySpin.LineSelector_Line2)
        # self.cam_primary.V3_3Enable.SetValue(True)

        # Set up secondary camera trigger
        self.cam_secondary.TriggerMode.SetValue(PySpin.TriggerMode_Off)
        # self.cam_secondary.TriggerSource.SetValue(PySpin.TriggerSource_Line3)
        # self.cam_secondary.TriggerOverlap.SetValue(PySpin.TriggerOverlap_ReadOut)
        # self.cam_secondary.TriggerMode.SetValue(PySpin.TriggerMode_On)
        

        # Set acquisition mode
        self.cam_primary.AcquisitionMode.SetValue(PySpin.AcquisitionMode_Continuous)
        self.cam_secondary.AcquisitionMode.SetValue(PySpin.AcquisitionMode_Continuous)

        # Start acquisition; note that secondary camera has to be started first so 
        # acquisition of primary camera triggers secondary camera.
        self.cam_secondary.BeginAcquisition()
        self.cam_primary.BeginAcquisition()

        #Start the video

        #Create a SpinVideo instance for both cameras
        self.avi_video_primary = PySpin.SpinVideo()
        self.avi_video_secondary = PySpin.SpinVideo()

        #Set filename and options for both videos
        filename_primary = 'SaveToAvi-MJPG-%s' % self.primary_sn
        filename_seconday = 'SaveToAvi-MJPG-19061546' 
        option_primary = PySpin.MJPGOption()
        option_secondary = PySpin.MJPGOption()
        option_primary.frameRate = 60
        option_secondary.frameRate = 60
        option_primary.quality = 75
        option_secondary.quality = 75

        #Open the recording file for both camera
        self.avi_video_primary.Open(filename_primary, option_primary)
        self.avi_video_secondary.Open(filename_seconday, option_secondary)


    # Handles the closing and deinitialization of both cameras and the avi video 
    def deoperate_cameras(self):

        #Wait on processes to finsih up the last of the appending

        #Print the number of dropped frames
        print("Total missed frames(Primary): %d" % self.missed_frames_p)
        print("Total missed frames(Secondary): %d" % self.missed_frames_s)

        #Close the recording files
        self.avi_video_primary.Close()
        self.avi_video_secondary.Close()

        # Stop acquisition
        self.cam_secondary.EndAcquisition()
        self.cam_primary.EndAcquisition()


        # De-initialize
        self.cam_primary.DeInit()
        self.cam_secondary.DeInit()

        # Delete Assets
        del self.cam_primary
        del self.cam_secondary
        del self.cam_list


    # While experiment is running, retrieves frames from the camera, puts them into the shared queue, and releses them from the buffer
    # TODO: Fails when try to aquire image using second camera
    def acquire_frames(self, q_p, q_s, cam_p, cam_s):
        while self.running_experiment:
            try:
                # Grab frames from primary camera's buffer
                buffer_image_p = cam_p.GetNextImage()

                # Grab frames from secondary camera's buffer
                buffer_image_s = cam_s.GetNextImage()

                # Store frames into shared queue for primary camera
                q_p.put(buffer_image_p)

                # Store frames into shared queue for secondary camera
                q_s.put(buffer_image_s)

                # Checks if the frames from the primary camera are sequential; Increments if the frames are not sequential
                if int(buffer_image_p.GetFrameID()) != (self.prev_frame_id_p + 1):
                    self.missed_frames_p += 1
                self.prev_frame_id_p = int(buffer_image_p.GetFrameID())

                # Checks if the frames from the secondary camera are sequential; Increments if the frames are not sequential
                if int(buffer_image_s.GetFrameID()) != (self.prev_frame_id_s + 1):
                    self.missed_frames_s += 1
                self.prev_frame_id_s = int(buffer_image_s.GetFrameID())

                # Release images from the buffers 
                buffer_image_p.Release()
                buffer_image_s.Release()

            except:
                pass


    # Using the shared queue and while experiment is running, dequeues frames and appends them to the end of the avi recording
    # TODO: Fails when try to aquire image using second camera
    def append_to_video(self, q_p, q_s):
        while self.running_experiment or not q_p.empty() or not q_s.empty():
            try:
                # Grab frames from the primary camera's shared queue
                queue_image_p = q_p.get()

                # Grab frames from the secondary camera's shared queue
                queue_image_s = q_s.get()

                # Append frames to the primary camera's avi video
                self.avi_video_primary.Append(queue_image_p)

                # Append frames to the secondary camera's avi video
                self.avi_video_secondary.Append(queue_image_s)

            except:
                pass


    # A function to handle all updating of values and functions
    def start_gui(self):
        # The experiment has started running
        self.running_experiment = True

        # Time the experiment was started
        self.start_time = datetime.datetime.now()

        # Update counter for the graph to keep measurements in time of one second
        self.seconds_interval = datetime.datetime.now()

        # Set the standard datetime format
        self.datetimeFormat = '%Y-%m-%d %H:%M:%S.%f'

        # Convert the given hz into milliseconds
        self.hz_to_mil = int((1/self.scan_hz.get())*1000)

        # Max items in Labjack values list = Twice the number of events per second
        self.max_items = 2 * self.scan_hz.get()

        # Analog input lists from the Labjack, initalized with 2x set hz rate of 0's 
        self.data_ain0 = [0] * self.max_items
        self.data_ain1 = [0] * self.max_items
        self.data_ain2 = [0] * self.max_items
        self.data_ain3 = [0] * self.max_items
        self.data_ain4 = [0] * self.max_items
        self.data_ain5 = [0] * self.max_items
        self.data_ain6 = [0] * self.max_items
        self.data_ain7 = [0] * self.max_items

        # Set an array to hold time incriments
        self.time_inc = []
        for x in np.arange(0.0, 2.0, 2/self.max_items):
            self.time_inc.append(x)

        # Create a subplot in the canvas f
        self.ax1 = self.f.add_subplot(1,1,1)

        # Call to initalize the Labjack
        self.init_labjack() 

        # Call to initialize cameras and avi video
        self.operate_cameras()

        # Start processes to begin the capturing from the Blackfly camera
        self.thread1 = threading.Thread(target= self.acquire_frames, args=(self.image_queue_primary, self.image_queue_secondary, self.cam_primary, self.cam_secondary, ), daemon= True)
        self.thread2 = threading.Thread(target= self.append_to_video, args=(self.image_queue_primary, self.image_queue_secondary, ), daemon= True)
        self.thread1.start()
        self.thread2.start()

        #Start writing data to a file 
        # self.write_to_file()

        #Call to update function to begin the animation of the GUI
        self.update_gui()


    # A function to stop the current experiment and revert the GUI back to a clean state
    def stop_gui(self):
        # The experiment is no longer running
        self.running_experiment = False

        # Wait for the processes to terminate
        self.thread1.join()
        self.thread2.join()

        # Call function to handle closing of the cameras and video
        self.deoperate_cameras()

        # Stops the call to update being made in update_gui
        self.root.after_cancel(self.update_after_call_id) 

        self.var0.set("0") # Resets voltage being read from the labjack at FIO0
        self.var1.set("0") # Resets voltage being read from the labjack at FIO1
        self.var2.set("0") # Resets voltage being read from the labjack at FIO2
        self.var3.set("0") # Resets voltage being read from the labjack at FIO3
        self.var4.set("0") # Resets voltage being read from the labjack at FIO4
        self.var5.set("0") # Resets voltage being read from the labjack at FIO5
        self.var6.set("0") # Resets voltage being read from the labjack at FIO6
        self.var7.set("0") # Resets voltage being read from the labjack at FIO7

        # Removes the subplot from the canvas, creates a clean subplot for looks
        self.ax1.clear()
        # Set fixed axis values
        self.ax1.set_xlim([0,2])
        self.ax1.set_ylim([-.5,5])
        #Label axes
        self.ax1.set_xlabel('time (s)')
        self.ax1.set_ylabel('amplitude')        
        self.canvas.draw()

        # Resets the scan hz entry
        self.scan_hz.set("Enter desired hz...")

        # Close all UD driver opened devices in the process
        LabJackPython.Close() 

        del self.image_queue_primary
        del self.image_queue_secondary

        gc.collect()


    # Holds the function calls that need to be updated based on hz
    def update_gui(self):
        
        # Updates the ainalog voltages being read in from the Labjack
        self.update_voltage()

        # Updates the graph of the analog voltages
        self.animate_with_stream()

        # Schedule for this function to call itself agin after 16 milliseconds ~ 60hz
        self.update_after_call_id = self.root.after(16, self.update_gui) 


    # Animates the graph using a stream of data from the labjack
    def animate_with_stream(self):
        # Lists for each analog to hold the newly streamed data
        new_data_ain0 = []
        new_data_ain1 = []
        new_data_ain2 = []
        new_data_ain3 = []
        new_data_ain4 = []
        new_data_ain5 = []
        new_data_ain6 = []
        new_data_ain7 = []

        # Stream in X hz events/second worth of data and extend it into the new data lists using a stream
        self.d.streamStart()
        for r in self.d.streamData():
            if r is not None:
                new_data_ain0.extend(r['AIN0'])
                new_data_ain1.extend(r['AIN1'])
                new_data_ain2.extend(r['AIN2'])
                new_data_ain3.extend(r['AIN3'])
                new_data_ain4.extend(r['AIN4'])
                new_data_ain5.extend(r['AIN5'])
                new_data_ain6.extend(r['AIN6'])
                new_data_ain7.extend(r['AIN7'])
            if len(new_data_ain0) >= self.scan_hz.get():
                break
        self.d.streamStop()

        #Extends on the new data into data
        self.data_ain0.extend(new_data_ain0)
        self.data_ain1.extend(new_data_ain1)
        self.data_ain2.extend(new_data_ain2)
        self.data_ain3.extend(new_data_ain3)
        self.data_ain4.extend(new_data_ain4)
        self.data_ain5.extend(new_data_ain5)
        self.data_ain6.extend(new_data_ain6)
        self.data_ain7.extend(new_data_ain7)

        #Remove older data from the front of the lists
        self.data_ain0 = self.data_ain0[-self.max_items:]
        self.data_ain1 = self.data_ain1[-self.max_items:]
        self.data_ain2 = self.data_ain2[-self.max_items:]
        self.data_ain3 = self.data_ain3[-self.max_items:]
        self.data_ain4 = self.data_ain4[-self.max_items:]
        self.data_ain5 = self.data_ain5[-self.max_items:]
        self.data_ain6 = self.data_ain6[-self.max_items:]
        self.data_ain7 = self.data_ain7[-self.max_items:]

        #Plot the array with new information on the graph 
        self.ax1.clear()

        #Set fixed axis values
        #self.ax1.set_xlim([0,2])
        self.ax1.set_ylim([-.5,5])

        #Label axes
        self.ax1.set_xlabel('time (s)')
        self.ax1.set_ylabel('amplitude')

        #Plot the new data for each analog
        self.ax1.plot(self.time_inc, self.data_ain0, label = 'AIN0')
        self.ax1.plot(self.time_inc, self.data_ain1, label = 'AIN1')
        self.ax1.plot(self.time_inc, self.data_ain2, label = 'AIN2')
        self.ax1.plot(self.time_inc, self.data_ain3, label = 'AIN3')
        self.ax1.plot(self.time_inc, self.data_ain4, label = 'AIN4')
        self.ax1.plot(self.time_inc, self.data_ain5, label = 'AIN5')
        self.ax1.plot(self.time_inc, self.data_ain6, label = 'AIN6')
        self.ax1.plot(self.time_inc, self.data_ain7, label = 'AIN7')

        #Create a legend for each analog to make dta tracking easier
        self.ax1.legend()

        #Display the new graph
        self.canvas.draw()
    

    #Handles an interrupt made during an experiment
    def on_closing(self):
        if self.running_experiment:
            self.stop_gui()
            self.root.destroy()
        else:
            self.root.destroy()


# MAIN - Creates a startup window and the main GUI. Passes variables from startup window to the main window
def main():

    # Make a call to the SettingsWindow class which starts the intial prompt screen to set the avtive directory
    # Properties: now, ad_var
    # Functions: prompt_window, update_window, submit_ad

    # Instance of a SettingsWindow
    startwindow = SettingsWindow() 

    # Call the propmt_window function to create the startup window
    startwindow.prompt_window()

    # Store the active directory set by the user into an easy to identify variable: ad
    ad = startwindow.ad_var.get()
    # Stores the serial number of the primary camera
    psn = startwindow.pcamera_var.get()
    # Stores the file split size
    fss = startwindow.splitsize_var.get()


    # Make a call to the UILabCapture class which contains functions for the main GUI window
    # Properties: None
    # Functions: init_labjack, update_voltage, build_window
    # app is a UILabCapture instance
    app = UILabCapture(ad, psn, fss) 

    #Call the build_window to create the main GUI window and starts the GUI
    app.build_window()

# Indicates that the python script will be run directly, and not imported by something else; Include an else to handle importing
if __name__ == '__main__':
    main()

