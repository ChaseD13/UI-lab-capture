import u3 
import LabJackPython
import time
import tkinter as tk
import datetime  #now.strftime("%Y-%m-%d %H:%M")
import matplotlib.figure as figure
import matplotlib.animation as animation
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import PySpin
import os


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


    #Labels for entry boxes
        tk.Label(self.root, text = "Date: ",).grid(row = 0, column = 0)
        tk.Label(self.root, text = "Vol Number: ").grid(row = 1, column = 0)
        tk.Label(self.root, text = "Active Directory: ").grid(row = 2, column = 0)


    #Entry boxes
        self.date_slot = tk.Entry(self.root, textvariable = self.date_var, justify = "left", width = 80) #Entry variable for setting the date.
        self.date_slot.grid(row = 0, column = 2)

        self.volnum_slot = tk.Entry(self.root, textvariable = self.volnum_var, justify = "left", width = 80) #Entry variable for setting the vole number. 
        self.volnum_slot.grid(row = 1, column = 2)

        self.ad_slot = tk.Entry(self.root, textvariable = self.ad_var, justify = "left", width = 80) #Entry variable that displays the current AD as it is being filled in.
        self.ad_slot.grid(row = 2, column = 2)

        tk.Button(self.root, text = "Submit", command = self.submit_ad).grid(row = 3, column = 0) #Button that when pressed closes the settings window

    #Function Calls

        self.update_window() #Call to update the window when the user types in new values into the entry fields.

        #Start the window
        self.root.mainloop() 

    #Function that updates 
    #TODO: Function causes errors after submit button is pushed
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
    def __init__(self, active_directory):
        self.filepath = active_directory #Active directory path is stored in a local varaible
 
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

        self.update_interval = 100 # Time (ms) between polling/animation updates
        self.max_elements = 1000    # Maximum number of elements to store in plot lists


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
        self.scan_scale = tk.Scale(self.labjack_values, from_=0.1, to=10, orient = tk.HORIZONTAL, label = "Scan rate (Hz)", length = 500, resolution = .2)
        self.scan_scale.grid(row = 3, column = 0, columnspan = 8)
        self.scan_scale.set(1)

        #Figure
        #Create Matplotlib figure and a set of axes to draw our plot on
        self.fig = figure.Figure(figsize = (6,6))
        self.fig.subplots_adjust(left=0.1, right = 0.8)
        self.ax1 = self.fig.add_subplot(1,1,1)

        #Variables
        self.xs = []
        self.volts = []
        self.hz = tk.DoubleVar()

        #Create a Tkinter widget out of that figure
        self.canvas = FigureCanvasTkAgg(self.fig, master = self.scrolling_graph)
        self.canvas_plot = self.canvas.get_tk_widget()

        self.canvas_plot.grid(row = 0, column = 0)

        # Periodically call FuncAnimation() to handle the polling and updating of the graph
        self.fargs = (self.ax1, self.xs, self.volts, self.hz)
        self.ani = animation.FuncAnimation(  self.fig, self.animate, fargs=self.fargs, interval=self.update_interval)


        #Function Calls

        #Call to initalize the labjack and its configuration 
        self.init_labjack() 


        #Call to the voltage test function to show the voltages being taken in by the labjack
        self.update_voltage()  

        self.write_to_file()


        #Start the window
        self.root.mainloop() 


    #Function to initialize the lab jack, get its configuration data, and set the FIO ports to analog.
    #try/except case is used to check if the labjack is able to be opened, if not a statement is preinted and the function closes the labjack 
    def init_labjack(self):
        try:
            self.d = u3.U3() #Connect to labjack 
            self.d.getCalibrationData() #Calibration data will be used by functions that convert binary data to voltage/temperature and vice versa
            self.d.configIO(FIOAnalog= 255) #Set the FIO to read in analog; 255 sets all eight FIO ports to analog

        except:
            LabJackPython.Close() #Close all UD driver opened devices in the process


    #Update voltage is used to constantly monitor the AIN0 port to see what voltage the port is reciving
    #It is adjusted by the scan_scale variable to scan faster or slower
    def update_voltage(self):
        #Try to set the update interval equal to the desired Hz converted into milliseconds
        try:
            self.update_interval =int((1/self.scan_scale.get())*1000)
        except:
            pass
    
        self.var.set(round(self.d.getAIN(0), 3)) #Get and set voltage for port 0
        self.var1.set(round(self.d.getAIN(1), 3)) #Get and set voltage for port 1
        self.var2.set(round(self.d.getAIN(2), 3)) #Get and set voltage for port 2
        self.var3.set(round(self.d.getAIN(3), 3)) #Get and set voltage for port 3
        self.var4.set(round(self.d.getAIN(4), 3)) #Get and set voltage for port 4
        self.var5.set(round(self.d.getAIN(5), 3)) #Get and set voltage for port 5
        self.var6.set(round(self.d.getAIN(6), 3)) #Get and set voltage for port 6
        self.var7.set(round(self.d.getAIN(7), 3)) #Get and set voltage for port 7

        self.ani = animation.FuncAnimation(  self.fig, self.animate, fargs=self.fargs, interval=self.update_interval)

        self.root.update() #Update the window
        self.root.after(self.update_interval, self.update_voltage) #Schedule for this function to call itself agin after update_interval milliseconds


    # This function is called periodically from FuncAnimation
    def animate(self, i, ax1, xs, volts, hz):

        # Update data to display temperature and light values
        new_volts = round(self.d.getAIN(0), 3)

        # Update the labels
        hz.set(new_volts)

        # Append timestamp to x-axis list
        self.timestamp = mdates.date2num(datetime.datetime.now())
        xs.append(self.timestamp)

        # Append sensor data to lists for plotting
        volts.append(new_volts)

        # Limit lists to a set number of elements
        xs = xs[-self.max_elements:]
        volts = volts[-self.max_elements:]

        # Clear, format, and plot light values first (behind)
        color = 'tab:red'
        ax1.clear()
        ax1.set_ylabel('Hz', color=color)
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.fill_between(xs, volts, 0, linewidth=2, color=color, alpha=0.3)

        # Format timestamps to be more readable
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        self.fig.autofmt_xdate()


    #
    def write_to_file(self):
        try:
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            with open(self.filepath, "w") as f:
                f.write("This is test data \n")
        finally:
            f.close()



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


    #Make a call to the UILabCapture class which contains functions for the main GUI window
    #app is a UILabCapture
    #properties: None
    #functions: init_labjack, update_voltage, build_window
    app = UILabCapture(ad) 
    #Call the build_window to create the main GUI window
    app.build_window()

    LabJackPython.Close() #Close all UD driver opened devices in the process

if __name__ == '__main__':
    main()
