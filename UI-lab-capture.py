import u3 
import LabJackPython
import time
import tkinter as tk
import datetime  #now.strftime("%Y-%m-%d %H:%M")
import matplotlib.figure as figure
import matplotlib.animation as animation
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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
        self.root.geometry("1000x600") 

    #Variables
        self.ad_var = tk.StringVar() #Holds the active directory string.

        self.date_var = tk.StringVar() #Holds the date string
        self.date_var.set(self.now.strftime("%Y-%m-%d")) #Sets that date variable to today's current date. Can be edited by the user.

        self.volnum_var = tk.StringVar() #Holds the Vole number. Assigned by the user.


    #Labels for entry boxes
        tk.Label(self.root, text = "Date: ",).grid(row = 0, column = 0)
        tk.Label(self.root, text = "Vol Number: ").grid(row = 1, column = 0)
        tk.Label(self.root, text = "Active Directory: ").grid(row = 2, column = 0)


    #Entry boxes
        self.date_slot = tk.Entry(self.root, textvariable = self.date_var, justify = "left", width = 40) #Entry variable for setting the date.
        self.date_slot.grid(row = 0, column = 2)

        self.volnum_slot = tk.Entry(self.root, textvariable = self.volnum_var, justify = "left", width = 40) #Entry variable for setting the vole number. 
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
        self.ad_var.set("c://Desktop/" + self.date_var.get() + "/" + self.volnum_var.get() + "/")
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
    # def __init__(self):
 
    #Builds the main GUI window 
    def build_window(self):
        #Initialize a window
        self.root = tk.Tk()


    #Style

        #Change the title of the window
        self.root.title("UI Lab Capture")
        # width x height + x_offset + y_offset:
        self.root.geometry("1000x1000") 


    #Variables

        #Var is the number being read in by the labjack 
        self.var = tk.IntVar() #Voltage being read from the labjack 
        self.update_interval = 400 # Time (ms) between polling/animation updates
        self.max_elements = 50     # Maximum number of elements to store in plot lists


    #Labels

        # Label that is filling the space where the camera will be
        self.cameras = tk.Label(self.root, text = "Space for Cameras", bg = "orange", height = 20)
        self.cameras.grid(rowspan = 10, columnspan = 10)

        #Labels for the AIN0 data value 
        tk.Label(self.root, text = "AIN0: ").grid(row = 11, column = 0)

        self.ain_zero = tk.Label(self.root, textvariable = self.var)
        self.ain_zero.grid(row = 11, column = 1)


    #Scales
        #Scale for users to adjust the scan speed in Hz
        self.scan_scale = tk.Scale(self.root, from_=.01, to=10, orient = tk.HORIZONTAL, label = "Hz", tickinterval = 0.25, length = 200)
        self.scan_scale.grid(row = 12, column = 0)
        self.scan_scale.set(2.5)

    #Figure
        #Create Matplotlib figure and a set of axes to draw our plot on
        self.fig = figure.Figure(figsize = (7,7))
        self.fig.subplots_adjust(left=0.1, right = 0.8)
        self.ax1 = self.fig.add_subplot(1,1,1)

        #Variables
        self.xs = []
        self.volts = []
        self.hz = tk.DoubleVar()

        #Create a Tkinter widget out of that figure
        self.canvas = FigureCanvasTkAgg(self.fig, master = self.root)
        self.canvas_plot = self.canvas.get_tk_widget()

        self.canvas_plot.grid(row = 11, column = 11, rowspan = 5, columnspan = 4, padx = 20)

        # Periodically call FuncAnimation() to handle the polling and updating of the graph
        self.fargs = (self.ax1, self.xs, self.volts, self.hz)
        self.ani = animation.FuncAnimation(  self.fig, self.animate, fargs=self.fargs, interval=self.update_interval)


    #Function Calls

        #Call to initalize the labjack and its configuration 
        self.init_labjack() 


        #Call to the voltage test function to show the voltages being taken in by the labjack
        self.update_voltage()  


        #Start the window
        self.root.mainloop() 


    #Function to initialize the lab jack, get its configuration data, and set the FIO ports to analog.
    #try/except case is used to check if the labjack is able to be opened, if not a statement is preinted and the function closes the labjack 
    def init_labjack(self):
        try:
            self.d = u3.U3() #Connect to labjack 
            self.d.getCalibrationData() #Calibration data will be used by functions that convert binary data to voltage/temperature and vice versa
            self.d.configIO(FIOAnalog= 15) #Set the FIO to read in analog
        except:
            LabJackPython.Close() #Close all UD driver opened devices in the process
            self.root.after(100, self.init_labjack()) #No labjack found OR labjack was not closed properly


    #Update voltage is used to constantly monitor the AIN0 port to see what voltage the port is reciving
    #It is adjusted by the scan_scale variable to scan faster or slower
    #TODO: Make this function more robust, I would imagine the user would want to uttalize multiple port
    def update_voltage(self):
        #Try to set the update interval equal to the desired Hz converted into milliseconds
        try:
            self.update_interval = int((1/self.scan_scale.get())*1000)
        except:
            pass
    
        self.var.set(self.d.getAIN(0)) #Asign the voltage to var
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
    app = UILabCapture() 
    #Call the build_window to create the main GUI window
    app.build_window()

    LabJackPython.Close() #Close all UD driver opened devices in the process

if __name__ == '__main__':
    main()