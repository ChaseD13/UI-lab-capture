import sys
import numpy as np
import PySpin
import multiprocessing
from tkinter import messagebox

def wr():
    file = open('testfile_P.txt','w') 
    file.write('Hello World from PCC')
    file.close()
    return 0

# Store passed arguments
# NOTE: sys.argv[0] is the script name
try:
    # Expected to recieve a camera object from the master script
    if isinstance(sys.argv[1], PySpin.Camera):
        primary_camera = sys.argv[1] 
    else:
        messagebox.showerror("Error", "Argument[1] passed to Primary_Camera_Control was not a PySpin.Camera object")
        #TODO: EXIT EXPERIMENT

    # Expected to recieve a multiprocessing Queue from the master script
    if isinstance(sys.argv[2], multiprocessing.Queue):
        shared_queue = sys.argv[2] 
    else:
        messagebox.showerror("Error", "Argument[2] passed to Primary_Camera_Control was not a multiprocessing.Queue object")
        #TODO: EXIT EXPERIMENT
except Exception as ex: 
    messagebox.showerror("Error", "%s" % ex)
        #TODO: EXIT EXPERIMENT
    
# Init Camera
primary_camera.Init()

# Retrieve GenICam nodemap
primary_nodemap = primary_camera.GetNodeMap()

# Retrieve nodemap TLDevice
primary_nodemaptldevice = primary_camera.GetTLDeviceNodeMap()

# Setup the hardware triggers
# NOTE: Turned off for now because gpio pins not connected

# # Set up primary camera trigger
# primary_camera.LineSelector.SetValue(PySpin.LineSelector_Line2)
# primary_camera.V3_3Enable.SetValue(True)

# Set acquisition mode
primary_camera.AcquisitionMode.SetValue(PySpin.AcquisitionMode_Continuous)

# Set aquisition rate to desired fps for both cameras
#TODO: Make this argument changeable
primary_camera.AcquisitionFrameRateEnable.SetValue(True)
primary_camera.AcquisitionFrameRate.SetValue(60)

primary_camera.BeginAcquisition()

#Start the video

#Create a SpinVideo instance for both cameras
avi_video_primary = PySpin.SpinVideo()

#Set filename and options for both videos
#TODO: Make the video path save to the working directory of the experiment
filename_primary = '/SaveToAvi-MJPG-primary'
option_primary = PySpin.MJPGOption()
option_primary.frameRate = 60
option_primary.quality = 75

#Open the recording file for both camera
avi_video_primary.Open(filename_primary, option_primary)

while True:
    # Acquire an image(s)
    image = primary_camera.GetNextImage()

    # Append to video
    avi_video_primary.Append(image)

    # Pipe/Send image(s) back to the master process
    shared_queue.put(image)