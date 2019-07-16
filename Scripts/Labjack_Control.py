from tkinter import messagebox, Tk
import LabJackPython
import os
import sys
import u3 


# Handles initializing the data output file, streaming data from the labjack, recording data in outputfile, and passing the data back to master
def run(running_experiment_queue, scan_frequency, start_time, voltage_values, file_name):
    # ~ VARIABLES ~
    time_incrementer = 0.000000
    tbs = 1.0/scan_frequency

    # ~ DATA FILE ~
    # Open a file at the selected file path; 
    file_io = open(file_name.value + '.dat', "w")
    
    # ~ FORMAT ~

    # Current date 
    file_io.write(start_time.strftime("%m/%d/%Y") + "\n")

    # Current time
    file_io.write(start_time.strftime("%I:%M:%S %p") + "\n" + "\n")

    # Channel Info
    for i in range(8):
        file_io.write("Insert channel info here... \n")
    
    # Add Spacer
    file_io.write("\n")

    #Labels for the tops of the channels seperated by three tabs
    file_io.write("Time\t\t   v0\t\t   v1\t\t   v2\t\t   v3\t\t   v4\t\t   v5\t\t   v6\t\t   v7\t\t   y0\t\t   y1\t\t   y2\t\t   y3\t\t   y4\t\t   y5\t\t   y6\t\t   y7 \n")

    # ~ LABJACK ~
    # Init Labjack
    labjack = u3.U3()
    # Calibration data will be used by functions that convert binary data to voltage/temperature and vice versa
    labjack.getCalibrationData() 
    # Set the FIO to read in analog; 255 sets all eight FIO ports to analog
    labjack.configIO(FIOAnalog= 255) 
    # Set the stream configuration
    # labjack.streamConfig(NumChannels= self.num_channels.get(), PChannels=range(self.num_channels.get()), NChannels=[31]*self.num_channels.get(), Resolution=1, ScanFrequency=self.scan_hz.get())
    labjack.streamConfig(NumChannels= 8, PChannels=range(8), NChannels=[31]*8, Resolution=1, ScanFrequency= scan_frequency)

    # ~ STREAM ~
    # Start labjack stream
    try:
        labjack.streamStart()
    except:
        labjack.streamStop()
        labjack.streamStart()
    
    # Stream the data into lists
    for r in labjack.streamData():
        # Lists for each analog to hold the newly streamed data
        new_data_ain0 = []
        new_data_ain1 = []
        new_data_ain2 = []
        new_data_ain3 = []
        new_data_ain4 = []
        new_data_ain5 = []
        new_data_ain6 = []
        new_data_ain7 = []
        time_stamps = []

        if r is not None:
            new_data_ain0.extend(r['AIN0'])
            new_data_ain1.extend(r['AIN1'])
            new_data_ain2.extend(r['AIN2'])
            new_data_ain3.extend(r['AIN3'])
            new_data_ain4.extend(r['AIN4'])
            new_data_ain5.extend(r['AIN5'])
            new_data_ain6.extend(r['AIN6'])
            new_data_ain7.extend(r['AIN7'])
        else:
            continue

        time_stamps = [time_incrementer + t * tbs for t in (range(len(new_data_ain7)))]

        # The current time for the next set of scans
        time_incrementer = time_stamps[-1] + tbs 

        # List to hold newly obtained data and time stamps
        data_list = [time_stamps, new_data_ain0, new_data_ain1, new_data_ain2, new_data_ain3, new_data_ain4, new_data_ain5, new_data_ain6, new_data_ain7]

        # Pipe/Send data back to master
        voltage_values.put(data_list)

        # Write the data 
        # Increments vertically
        for i in range(len(data_list[-1])):
            # Increments horizontally
            for j in range(len(data_list)):
                # If not last list, print with with tabs
                if j != (len(data_list) - 1):
                    # self.f.write(str(round(data_list[j][i], 6)) + "\r\t")
                    file_io.write('{:.6f}'.format(round(data_list[j][i], 6)) + "\t")
                # Else print with no tabs and end line
                else:
                    file_io.write(str(round(data_list[j][i], 6)))
                    file_io.write("\n")

        # Break out of loop if experiment is done
        if not running_experiment_queue.empty():
            break

    # ~ CLOSE ~
    # Stop stream
    labjack.streamStop()

    # Close the data file
    file_io.close()

    # Close all UD driver opened devices in the process
    LabJackPython.Close() 
