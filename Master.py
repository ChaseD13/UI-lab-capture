from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
import multiprocessing
import matplotlib.figure as figure
import numpy as np
import os
import PySpin
import queue as Queue
import sys
import tkinter as tk 
import u3
import Labjack_Control
import Primary_Camera_Control
import Secondary_Camera_Control


# Window to take in user input and apply settings for the experiment
# Properties: now, ad_var
# Functions: build_window, update_window, submit_ad
class SettingsWindow():
    def __init__(self):
        self.now = datetime.datetime.now()
        self.cont = True
        
    def build_window(self):
        #Initialize a window
        self.root = tk.Tk()

        #Change the title of the window
        self.root.title("Active Directory and Other Settings")

        #width x height + x_offset + y_offset:
        self.root.geometry("1000x1000+0+0")
        self.root.state('zoomed')

        #Variables
        self.ad_var = tk.StringVar() #Holds the active directory string.

        self.wd_var = tk.StringVar() #Holds the working directory ex. "C:\Users\Behavior Scoring\Desktop" or "C://Users/Behavior Scoring/Desktop"
        self.wd_var.set('C://Users/Behavior Scoring/Desktop/UI-lab-capture')

        self.basefile_var = tk.StringVar() #Holds the basefile name ex. Test.txt
        
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

        #Handle interrupt 
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        #Start the window
        self.root.mainloop() 

    #Function that updates 
    def update_window(self):
        self.ad_var.set(self.wd_var.get() + "/" + self.basefile_var.get() + ".dat")
        self.after_event = self.root.after(5, self.update_window)
        self.root.update()

    #Function to close the window and confirm the active directory being used by the user 
    def submit_ad(self):
        self.root.after_cancel(self.after_event)
        self.root.destroy()

    def on_closing(self):
        self.cont = False
        self.root.destroy()


#
class MainWindow():
    # Initialization; Takes in an active directory path as a parameter
    def __init__(self, active_directory, primary_serial_number, fss, bsfl, wd):
        self.filepath = active_directory # Active directory path is stored in a local varaible
        self.primary_camera_serial_number = primary_serial_number # The serial number of the primary Blackfly S camera
        self.file_split_size = fss # The size of the file split
        self.filename = bsfl # Holds the basefile name from the settings window
        self.working_directory = wd # Holds the file path designated by the user
        self.experiment_in_progress = False # Bool; Indicates when an experiment is happening(True) or not(False) 


    # Used to create and format the filesystem using information provided from the settings window
    def create_filesystem(self):
        try:
            #Create a folder to hold all aquired data
            os.makedirs(self.working_directory)
        except OSError as ex:
            tk.messagebox.showerror("Error", '%s' % ex)
            #TODO: EXIT EXPERIMENT

        try:
            #Record working directory into the LOG.md
            # Open a file at the selected file path; If it dne, create a new one
            self.file_log = open(self.working_directory + '/LOG.txt', "a+")
            self.file_log.write( self.working_directory + '\n')
            self.file_log.close()
        except OSError as ex: 
            tk.messagebox.showerror("Error", '%s' % ex)
            #TODO: EXIT EXPERIMENT


    # Builds the main GUI window 
    def build_window(self):
        # Initialize a window
        self.root = tk.Tk()

        #Frame for Camera Preview
        self.camera_frame = tk.Frame(self.root)
        self.camera_frame.pack(side = "top", fill = "x")

        #Frame to hold Labjack data readings, start/stop buttons, and the user input for scan hz and fps
        self.labjack_values = tk.Frame(self.root)
        self.labjack_values.pack(side = "left", expand = True, fill = "both")

        # Frame to hold graph
        self.scrolling_graph = tk.Frame(self.root)
        self.scrolling_graph.pack(side = "right", expand = True, fill = "both")

        # ~STYLE~

        # Change the title of the window
        self.root.title("UI Lab Capture")
        # width x height + x_offset + y_offset:
        self.root.geometry("1000x1000+0+0") 
        self.root.state('zoomed')


        # ~VARIABLES~

        self.var0 = tk.IntVar() # Voltage being read from the labjack at FIO0
        self.var1 = tk.IntVar() # Voltage being read from the labjack at FIO1
        self.var2 = tk.IntVar() # Voltage being read from the labjack at FIO2
        self.var3 = tk.IntVar() # Voltage being read from the labjack at FIO3
        self.var4 = tk.IntVar() # Voltage being read from the labjack at FIO4
        self.var5 = tk.IntVar() # Voltage being read from the labjack at FIO5
        self.var6 = tk.IntVar() # Voltage being read from the labjack at FIO6
        self.var7 = tk.IntVar() # Voltage being read from the labjack at FIO7

        # ~ELEMENTS~

        # Frame to hold primary camera images
        self.img_p = tk.Label(self.camera_frame)
        self.img_p.pack(padx = 20, pady = 20, side = 'left', fill = 'both', expand = 1)

        # Frame to hold secondary camera images
        self.img_s = tk.Label(self.camera_frame)
        self.img_s.pack(padx = 20, pady = 20, side = 'left', fill = 'both', expand = 1)

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

        # Labl and entry for the labjack scan rate in hz
        tk.Label(self.labjack_values, text= 'Labjack Scan Rate:').pack()
        self.scan_hz = tk.IntVar()
        self.scan_hz.set("200")
        self.scan_space = tk.Entry(self.labjack_values, textvariable = self.scan_hz)
        self.scan_space.pack(padx = 10, pady = 10)

        # Labl and entry for the Blackfly cameras fps
        tk.Label(self.labjack_values, text= 'BlackFly FPS:').pack()
        self.frame_rate_input = tk.IntVar()
        self.frame_rate_input.set("60")
        self.scan_space = tk.Entry(self.labjack_values, textvariable = self.frame_rate_input)
        self.scan_space.pack(padx = 10, pady = 10)

        # Start and Stop buttons
        tk.Button(self.labjack_values, text = "Start Experiment", command = self.begin_experiment).pack(padx = 10, pady = 10)
        tk.Button(self.labjack_values, text = "Stop Experiment", command = self.end_experiment).pack(padx = 10, pady = 10)

        # Total time experied
        self.time_label = tk.IntVar()
        self.time_label.set('0 minute(s), 0 seconds')
        tk.Label(self.labjack_values, text= 'Experiment Time:').pack(padx = 10, pady = 10)
        tk.Label(self.labjack_values, textvariable= self.time_label).pack(padx = 10, pady = 10)

        # Data readings figure
        self.f = figure.Figure(figsize = (4,3))

        # Create a canvas in the window to place the figure onto
        self.canvas = FigureCanvasTkAgg(self.f, self.scrolling_graph)
        self.canvas.get_tk_widget().pack(side = "top", fill = "both", expand = True)
        self.canvas.draw()

        #Handle interrupt 
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Start the window
        self.root.mainloop()


    # Executed when the user clicks the start button
    # TODO: run_process works by itself. Trouble comes from the multiprocess part of the code
    def begin_experiment(self):
        # Running experiment
        self.experiment_in_progress = True

        # change the current working directory to specified path 
        os.chdir('C://Users/Behavior Scoring/Desktop/UI-lab-capture') 

        # Initialize variables to pass to the processes
        self.man = multiprocessing.Manager()
        self.shared_queue = self.man.Queue()
        
        # Get system
        self.system = PySpin.System.GetInstance()
        # Get camera list
        self.cam_list = self.system.GetCameras()
        # Figure out which is primary and secondary
        if self.cam_list.GetByIndex(0).TLDevice.DeviceSerialNumber() == str(self.primary_camera_serial_number):
            self.cam_primary = self.cam_list.GetByIndex(0)
            self.cam_secondary = self.cam_list.GetByIndex(1)
        else:
            self.cam_primary = self.cam_list.GetByIndex(1)
            self.cam_secondary = self.cam_list.GetByIndex(0)

        self.processes = [None] * 3  
        self.processes[0] = multiprocessing.Process(target=Labjack_Control.run)
        self.processes[1] = multiprocessing.Process(target=Secondary_Camera_Control.run)
        self.processes[2] = multiprocessing.Process(target=Primary_Camera_Control.run)
        for i in range(3):
            self.processes[i].start()


    # Given a script name, this spawns a sepearte process running the given script name
    def run_process(self, process):   
        print("Spawned %s" % process)                                                          
        os.system('python {}'.format(process))  


    # Executed when the user clicks the stop button
    def end_experiment(self): 
        self.experiment_in_progress = False
        #self.pool.terminate()
        #self.pool.join()
        for i in range(3):
            self.processes[i].join()
        print('Done!')  


    # Handles when the main window is closed via the exit button on the main window
    def on_close(self): 
        # Safely close the experiment when the exit button is clicked
        if self.experiment_in_progress:
            self.end_experiment()
        else:
            self.root.destroy()
                                      

# MAIN - Creates a startup window and the main GUI. Passes variables from startup window to the main window
# TODO: Better way to loop experiment calls; 
def main():
    while True:
        # Instance of a SettingsWindow
        startwindow = SettingsWindow() 

        # Call the propmt_window function to create the startup window
        startwindow.build_window()

        if startwindow.cont:
            # Store the active directory set by the user into an easy to identify variable: ad
            ad = startwindow.ad_var.get()
            # Stores the serial number of the primary camera
            psn = startwindow.pcamera_var.get()
            # Stores the file split size
            fss = startwindow.splitsize_var.get()
            # Stores the base file name
            bsfl = startwindow.basefile_var.get()
            # Get the file path for the working directory 
            wd = startwindow.wd_var.get()


            # Make a call to the UILabCapture class which contains functions for the main GUI window
            # Properties: None
            # Functions: init_labjack, update_voltage, build_window
            # app is a UILabCapture instance
            app = MainWindow(ad, psn, fss, bsfl, wd) 

            # Setup the filesystem for the files about to be produced by the current expereiment
            app.create_filesystem()

            #Call the build_window to create the main GUI window and starts the GUI
            app.build_window()
        else:
            return 0


# Indicates that the python script will be run directly, and not imported by something else; Include an else to handle importing
if __name__ == '__main__':
    main()
