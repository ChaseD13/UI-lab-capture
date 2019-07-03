import u3 
import LabJackPython
import sys
from tkinter import messagebox, Tk

    
def run(running_experiment_queue):
    file = open('testfile_L_run.txt','w') 
    file.write('Hello World from LC; In run!')
    file.close()

    # # Store passed arguments
    # # NOTE: sys.argv[0] is the script name
    # # Expected to recieve a camera object from the master script
    # try:
    #     if isinstance(lj, u3.U3):
    #         labjack = lj 
    #     else:
    #         messagebox.showerror("Error", "Argument[1] passed to Labjack_Control was not a u3.U3 object")
    #         # Close/End processes
    # except Exception as ex: 
    #     messagebox.showerror("Error", "%s" % ex)
    #         #TODO: EXIT EXPERIMENT

    labjack = u3.U3()

    # Init Labjack
    # TODO: ScanFreq set by user
    labjack.getCalibrationData() # Calibration data will be used by functions that convert binary data to voltage/temperature and vice versa
    labjack.configIO(FIOAnalog= 255) # Set the FIO to read in analog; 255 sets all eight FIO ports to analog
    # labjack.streamConfig(NumChannels= self.num_channels.get(), PChannels=range(self.num_channels.get()), NChannels=[31]*self.num_channels.get(), Resolution=1, ScanFrequency=self.scan_hz.get())
    labjack.streamConfig(NumChannels= 8, PChannels=range(8), NChannels=[31]*8, Resolution=1, ScanFrequency=200)

    # Stream the data
    try:
        labjack.streamStart()
    except:
        labjack.streamStop()
        labjack.streamStart()

    for r in labjack.streamData():
        if r is not None:
            #new_data_ain0.extend(r['AIN0'])
            pass
        else:
            pass

        # Write the data 

        #Pipe/Send data back to master

        if not running_experiment_queue.empty():
            labjack.streamStop()


