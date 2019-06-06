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

# MAX_REQUESTS is the number of packets to be read.
MAX_REQUESTS = 75
# SCAN_FREQUENCY is the scan frequency of stream mode in Hz
SCAN_FREQUENCY = 5000

#Add funtions purpose here....
#Properties: now, ad_var
#Functions: prompt_window, update_window, submit_ad
#Explanantion: Active directory is used as a term to describe the directory set by the user where they want to save various files
#References: "Settings window", 
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

        self.date_var = tk.StringVar() #Holds the date string
        self.date_var.set(self.now.strftime("%Y-%m-%d")) #Sets that date variable to today's current date. Can be edited by the user.

        self.volnum_var = tk.StringVar() #Holds the Vole number. Assigned by the user.
        self.volnum_var.set(1)

        self.pcamera_var = tk.IntVar() #Holds the Vole number. Assigned by the user.
        self.pcamera_var.set(19061331)


        #Labels for entry boxes
        tk.Label(self.root, text = "Date: ",).grid(row = 0, column = 0, padx = 10, pady = 10)
        tk.Label(self.root, text = "Vol Number: ").grid(row = 1, column = 0, padx = 10, pady = 10)
        tk.Label(self.root, text = "Active Directory: ").grid(row = 2, column = 0, padx = 10, pady = 10)
        tk.Label(self. root, text = "Primary Camera Serial Number: ").grid(row = 3, column = 0, padx = 10, pady = 10) 


        #Entry boxes
        self.date_slot = tk.Entry(self.root, textvariable = self.date_var, justify = "left", width = 80) #Entry variable for setting the date.
        self.date_slot.grid(row = 0, column = 2, padx = 10, pady = 10)

        self.volnum_slot = tk.Entry(self.root, textvariable = self.volnum_var, justify = "left", width = 80) #Entry variable for setting the vole number. 
        self.volnum_slot.grid(row = 1, column = 2, padx = 10, pady = 10)

        self.ad_slot = tk.Entry(self.root, textvariable = self.ad_var, justify = "left", width = 80) #Entry variable that displays the current AD as it is being filled in.
        self.ad_slot.grid(row = 2, column = 2, padx = 10, pady = 10)

        self.primary_slot = tk.Entry(self.root, textvariable = self.pcamera_var, justify = "left", width = 80) #Entry variable for setting the primary camera's serial number 
        self.primary_slot.grid(row = 3, column = 2, padx = 10, pady = 10)

        tk.Button(self.root, text = "Submit", command = self.submit_ad).grid(row = 4, column = 0, padx = 20, pady = 10) #Button that when pressed closes the settings window

        #Function Calls

        self.update_window() #Call to update the window when the user types in new values into the entry fields.

        #Start the window
        self.root.mainloop() 

    #Function that updates 
    def update_window(self):
        self.ad_var.set("C:/Users/Behavior Scoring/Desktop/UI-lab-capture/" + self.date_var.get() + "/" + self.volnum_var.get() + ".txt")
        self.after_event = self.root.after(5, self.update_window)
        self.root.update()

    #Function to close the window and confirm the active directory being used by the user 
    def submit_ad(self):
        self.root.after_cancel(self.after_event)
        self.root.destroy()
    
    
#Add funtions purpose here....
#Properties: None
#Functions: init_labjack, update_voltage, build_window, animate
class UILabCapture():
    #Initialization; Takes in an active directory path as a parameter
    def __init__(self, active_directory, primary_serial_number):
        self.filepath = active_directory #Active directory path is stored in a local varaible
        self.primary_sn = primary_serial_number #The serial number of the primary Blackfly S camera
        self.update_interval = 100 #Time (ms) between polling/animation updates
        self.max_elements = 20   #Maximum number of elements to store in plot lists
 
    #Builds the main GUI window 
    def build_window(self):
        #Initialize a window
        self.root = tk.Tk()
        
        self.camera_frame = tk.Frame(self.root)
        self.camera_frame.grid(row = 0, column = 0, padx =10, pady = 10)
        self.camera_frame.grid_rowconfigure(0, weight = 1)
        self.camera_frame.grid_columnconfigure(0, weight = 1)

        self.labjack_values = tk.Frame(self.root)
        self.labjack_values.grid(row = 1, column = 0, padx = 10, pady = 10)
        self.labjack_values.grid_rowconfigure(0, weight = 1)
        self.labjack_values.grid_columnconfigure(0, weight = 1)

        self.scrolling_graph = tk.Frame(self.root)
        self.scrolling_graph.grid(row = 1, column = 1, padx= 10, pady = 10)
        self.scrolling_graph.grid_rowconfigure(0, weight = 1)
        self.scrolling_graph.grid_columnconfigure(0, weight = 1)


        #Style

        #Change the title of the window
        self.root.title("UI Lab Capture")
        # width x height + x_offset + y_offset:
        self.root.geometry("1000x1000+0+0") 
        self.root.state('zoomed')


        #Variables

        self.var = tk.IntVar() #Voltage being read from the labjack at FIO0
        self.var1 = tk.IntVar() #Voltage being read from the labjack at FIO1
        self.var2 = tk.IntVar() #Voltage being read from the labjack at FIO2
        self.var3 = tk.IntVar() #Voltage being read from the labjack at FIO3
        self.var4 = tk.IntVar() #Voltage being read from the labjack at FIO4
        self.var5 = tk.IntVar() #Voltage being read from the labjack at FIO5
        self.var6 = tk.IntVar() #Voltage being read from the labjack at FIO6
        self.var7 = tk.IntVar() #Voltage being read from the labjack at FIO7


        #Labels

        # Label that is filling the space where the camera will be
        self.cameras = tk.Label(self.camera_frame, text = "Space for Cameras", bg = "orange", height = 20)
        self.cameras.grid(row = 0, column = 0)

        #Labels for the FIO 0-7 ports on the labjacks
        tk.Label(self.labjack_values, text = "AIN0: ").grid(row = 0, column = 0)
        tk.Label(self.labjack_values, text = "AIN1: ").grid(row = 0, column = 1)
        tk.Label(self.labjack_values, text = "AIN2: ").grid(row = 0, column = 2)
        tk.Label(self.labjack_values, text = "AIN3: ").grid(row = 0, column = 3)
        tk.Label(self.labjack_values, text = "AIN4: ").grid(row = 0, column = 4)
        tk.Label(self.labjack_values, text = "AIN5: ").grid(row = 0, column = 5)
        tk.Label(self.labjack_values, text = "AIN6: ").grid(row = 0, column = 6)
        tk.Label(self.labjack_values, text = "AIN7: ").grid(row = 0, column = 7)

        self.ain_zero = tk.Label(self.labjack_values, textvariable = self.var)
        self.ain_zero.grid(row = 1, column = 0)

        self.ain_one = tk.Label(self.labjack_values, textvariable = self.var1)
        self.ain_one.grid(row = 1, column = 1)

        self.ain_two = tk.Label(self.labjack_values, textvariable = self.var2)
        self.ain_two.grid(row = 1, column = 2)

        self.ain_three = tk.Label(self.labjack_values, textvariable = self.var3)
        self.ain_three.grid(row = 1, column = 3)

        self.ain_four = tk.Label(self.labjack_values, textvariable = self.var4)
        self.ain_four.grid(row = 1, column = 4)

        self.ain_five = tk.Label(self.labjack_values, textvariable = self.var5)
        self.ain_five.grid(row = 1, column = 5)

        self.ain_six = tk.Label(self.labjack_values, textvariable = self.var6)
        self.ain_six.grid(row = 1, column = 6)

        self.ain_seven = tk.Label(self.labjack_values, textvariable = self.var7)
        self.ain_seven.grid(row = 1, column = 7)



        #Scales
        #Scale for users to adjust the scan speed in Hz
        # self.scan_scale = tk.Scale(self.labjack_values, from_=0.1, to=100, orient = tk.HORIZONTAL, label = "Scan rate (Hz)", length = 500, resolution = 1)
        # self.scan_scale.grid(row = 3, column = 0, columnspan = 8)
        # self.scan_scale.set(1)

        self.scan_hz = tk.IntVar()
        tk.Entry(self.labjack_values, textvariable = self.scan_hz).grid(row = 3, column = 0, columnspan = 2)

        #Button
        tk.Button(self.labjack_values, text = "Start Experiment", command = self.start_gui).grid(row = 4, column = 0, padx = 20, pady = 10) 
        tk.Button(self.labjack_values, text = "Stop Experiment", command = self.stop_gui).grid(row = 4, column = 1, padx = 20, pady = 10) 

        #Start the window
        self.root.mainloop() 


    #Function to initialize the lab jack, get its configuration data, and set the FIO ports to analog.
    #try/except case is used to check if the labjack is able to be opened, if not a statement is preinted and the function closes the labjack 
    def init_labjack(self):
        try:
            self.d = u3.U3() #Connect to labjack 
            self.d.getCalibrationData() #Calibration data will be used by functions that convert binary data to voltage/temperature and vice versa
            self.d.configIO(FIOAnalog= 255) #Set the FIO to read in analog; 255 sets all eight FIO ports to analog
            self.d.streamConfig(NumChannels=8, PChannels=[0, 1, 2, 3, 4, 5, 6, 7], NChannels=[31, 31, 31, 31, 31, 31, 31, 31], Resolution=3, ScanFrequency=self.scan_hz.get())
            
        except:
            LabJackPython.Close() #Close all UD driver opened devices in the process


    #Update voltage is used to constantly monitor the AIN0 port to see what voltage the port is reciving
    #It is adjusted by the scan_scale variable to scan faster or slower
    def update_voltage(self):
        #Try to set the update interval equal to the desired Hz converted into milliseconds
        # try:
        #     self.update_interval =int((1/self.scan_scale.get())*1000)
        # except:
        #     pass
        try:
            self.var.set(round(self.d.getAIN(0), 3)) #Get and set voltage for port 0
            self.var1.set(round(self.d.getAIN(1), 3)) #Get and set voltage for port 1
            self.var2.set(round(self.d.getAIN(2), 3)) #Get and set voltage for port 2
            self.var3.set(round(self.d.getAIN(3), 3)) #Get and set voltage for port 3
            self.var4.set(round(self.d.getAIN(4), 3)) #Get and set voltage for port 4
            self.var5.set(round(self.d.getAIN(5), 3)) #Get and set voltage for port 5
            self.var6.set(round(self.d.getAIN(6), 3)) #Get and set voltage for port 6
            self.var7.set(round(self.d.getAIN(7), 3)) #Get and set voltage for port 7
        except: 
            self.d.streamStop()
            self.update_voltage()

        # self.ani = animation.FuncAnimation(self.fig, self.animate, fargs=self.fargs, interval=self.update_interval)

        #self.root.update() #Update the window
        #self.root.after(self.update_interval, self.update_voltage) #Schedule for this function to call itself agin after update_interval milliseconds


    #Function to wrtie the data out to a directory
    def write_to_file(self):
        try:
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            with open(self.filepath, "w") as f:
                f.write("This is test data \n")
        finally:
            f.close()


    #Produces an image in the current working directory: primary.png
    #TODO: Add second camera to test functionality of the primary and secondary triggers.
    def operate_cameras(self):
        # Get system
        self.system = PySpin.System.GetInstance()
        # Get camera list
        self.cam_list = self.system.GetCameras()
        # Figure out which is primary and secondary
        if self.cam_list.GetByIndex(0).TLDevice.DeviceSerialNumber() == str(self.primary_sn):
            self.cam_primary = self.cam_list.GetByIndex(0)
            # self.cam_secondary = self.cam_list.GetByIndex(1)
        else:
            self.cam_primary = self.cam_list.GetByIndex(1)
            # self.cam_secondary = self.cam_list.GetByIndex(0)
 
        # Initialize cameras
        self.cam_primary.Init()
        # self.cam_secondary.Init()

        #retrieve GenICam nodemap
        self.primary_nodemap = self.cam_primary.GetNodeMap()


        #Setup the hardware triggers

        # Set up primary camera trigger
        self.cam_primary.LineSelector.SetValue(PySpin.LineSelector_Line2)
        self.cam_primary.V3_3Enable.SetValue(True)

        # Set up secondary camera trigger
        '''
        cam_secondary.TriggerMode.SetValue(PySpin.TriggerMode_Off)
        cam_secondary.TriggerSource.SetValue(PySpin.TriggerSource_Line3)
        cam_secondary.TriggerOverlap.SetValue(PySpin.TriggerOverlap_ReadOut)
        cam_secondary.TriggerMode.SetValue(PySpin.TriggerMode_On)
        '''

        # Set acquisition mode
        self.cam_primary.AcquisitionMode.SetValue(PySpin.AcquisitionMode_Continuous)
        #cam_secondary.AcquisitionMode.SetValue(PySpin.AcquisitionMode_SingleFrame)

        # Start acquisition; note that secondary camera has to be started first so 
        # acquisition of primary camera triggers secondary camera.
        #cam_secondary.BeginAcquisition()
        self.cam_primary.BeginAcquisition()

        # Acquire images
        self.image_primary = self.cam_primary.GetNextImage()
        #image_secondary = cam_secondary.GetNextImage()

        # Save images
        self.image_primary.Save('primary.png')
        #image_secondary.Save('secondary.png')

        image = Image.open('primary.png')
        photo = ImageTk.PhotoImage(image)
        img = tk.Label(self.camera_frame, image = photo)
        img.image = photo
        img.grid(row = 0, column = 0)

        # Stop acquisition
        self.cam_primary.EndAcquisition()
        #cam_secondary.EndAcquisition()

        # De-initialize
        self.cam_primary.DeInit()
        #cam_secondary.DeInit()

        # Clear references to images and cameras
        del self.image_primary
        #del image_secondary
        del self.cam_primary
        #del cam_secondary
        del self.cam_list


    #A function to handle all updating of values and functions
    def start_gui(self):
        #Convert the given hz into milliseconds
        self.hz_to_mil = int((1/self.scan_hz.get())*1000)

        #Limit of how many items we can have in the list
        self.max_items = 2 * self.scan_hz.get()

        #List with 2x times the hz rate 
        self.data = [0] * self.max_items

        #Set an array to hold time incriments
        self.time_inc = []
        for x in np.arange(0.0, 2.0, 2/self.max_items):
            self.time_inc.append(x)

        # self.max_samples = 2 * self.scan_hz.get()

        #Call to initalize the labjack and its configuration 
        self.init_labjack() 

        #Call to initialize cameras and to capture an image
        #self.operate_cameras()


        #self.start_figure()


        #Start writing data to a file 
        # self.write_to_file()

        self.update_gui()


    #A function to stop the current experiment and revert the GUI back to a clean state
    def stop_gui(self):
        self.root.after_cancel(self.update_after_call_id) #Stops the call to update being made in update_gui
        #self.ani.event_source.stop() #Stops the call to update being made in animate 

        self.var.set("") #Voltage being read from the labjack at FIO0
        self.var1.set("") #Voltage being read from the labjack at FIO1
        self.var2.set("") #Voltage being read from the labjack at FIO2
        self.var3.set("") #Voltage being read from the labjack at FIO3
        self.var4.set("") #Voltage being read from the labjack at FIO4
        self.var5.set("") #Voltage being read from the labjack at FIO5
        self.var6.set("") #Voltage being read from the labjack at FIO6
        self.var7.set("") #Voltage being read from the labjack at FIO7

        #TODO: Remove/Clean graph on stop experiment


    #Holds the function calls that need to be updated based on hz
    def update_gui(self):
        
        #Call to the voltage test function to show the voltages being taken in by the labjack
        self.update_voltage()

        #start time - if time now - time when started is one second call animate?
        self.animate_with_stream()

        self.update_after_call_id = self.root.after(self.hz_to_mil, self.update_gui) #Schedule for this function to call itself agin after update_interval milliseconds


    #Animates the graph using a stream of data from the labjack
    def animate_with_stream(self):

        ax = np.arange(1,365,1)
        #List to hold the newly streamed data
        new_data = []

        #Stream in X hz events/second worth of data and extend it into the new data list
        self.d.streamStart()
        for r in self.d.streamData():
            if r is not None:
                new_data.extend(r['AIN0'])
            if len(new_data) >= self.scan_hz.get():
                break
        self.d.streamStop()
        #print(new_data)

        #Extends on the new data into data
        self.data.extend(new_data)

        #Remove older data
        self.data = self.data[-self.max_items:]

        #Plot the array with new information on the graph 
        # f = figure.Figure(figsize=(5,5))
        # ax.plot(self.data)
        f = figure.Figure(figsize = (5,4))
        ax1 = f.add_subplot(1,1,1)
        ax1.plot(self.time_inc, self.data)

        #ax1.set_xlim([0,2])
        ax1.set_ylim([-.5,5])

        canvas = FigureCanvasTkAgg(f, self.scrolling_graph)
        canvas.get_tk_widget().grid(row = 0, column = 0)
        canvas.draw()





def main():

    #Variables
    ad = "" #Used to store the active directory. Simplifies the usage of the active directory from the settings window

    #Make a call to the SettingsWindow class which starts the intial prompt screen to set the avtive directory
    #Properties: now, ad_var
    #Functions: prompt_window, update_window, submit_ad
    startwindow = SettingsWindow() #Instance of a SettingsWindow
    #Call the propmt_window function to create the window
    startwindow.prompt_window()
    #Store the active directory set by the user into an easy to identify variable: ad
    ad = startwindow.ad_var.get()
    psn = startwindow.pcamera_var.get()


    #Make a call to the UILabCapture class which contains functions for the main GUI window
    #app is a UILabCapture
    #properties: None
    #functions: init_labjack, update_voltage, build_window
    app = UILabCapture(ad, psn) 
    #Call the build_window to create the main GUI window
    app.build_window()

    LabJackPython.Close() #Close all UD driver opened devices in the process

if __name__ == '__main__':
    main()
