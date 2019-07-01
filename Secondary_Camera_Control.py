import sys
import PySpin
import multiprocessing
from tkinter import messagebox

# Store passed arguments
# NOTE: sys.argv[0] is the script name
# Expected to recieve a camera object from the master script
if isinstance(sys.argv[1], PySpin.Camera):
    secondary_camera = sys.argv[1] 
else:
    messagebox.showerror("Error", "Argument[1] passed to Secondary_Camera_Control was not a PySpin.Camera object")
    #TODO: EXIT EXPERIMENT

# Expected to recieve a multiprocessing Queue from the master script
if isinstance(sys.argv[2], multiprocessing.Queue):
    shared_queue = sys.argv[2] 
else:
    messagebox.showerror("Error", "Argument[2] passed to Secondary_Camera_Control was not a multiprocessing.Queue object")
    #TODO: EXIT EXPERIMENT
    
# Init Camera
secondary_camera.Init()

# Retrieve GenICam nodemap
primary_nodemap = secondary_camera.GetNodeMap()

# Retrieve nodemap TLDevice
primary_nodemaptldevice = secondary_camera.GetTLDeviceNodeMap()

# Setup the hardware triggers
# NOTE: Turned off for now because gpio pins not connected

# # Set up primary camera trigger
# secondary_camera.LineSelector.SetValue(PySpin.LineSelector_Line2)
# secondary_camera.V3_3Enable.SetValue(True)

# Set acquisition mode
secondary_camera.AcquisitionMode.SetValue(PySpin.AcquisitionMode_Continuous)

# Set aquisition rate to desired fps for both cameras
#TODO: Make this argument changeable
secondary_camera.AcquisitionFrameRateEnable.SetValue(True)
secondary_camera.AcquisitionFrameRate.SetValue(60)

secondary_camera.BeginAcquisition()

#Start the video

#Create a SpinVideo instance for both cameras
avi_video_secondary = PySpin.SpinVideo()

#Set filename and options for both videos
#TODO: Make the video path save to the working directory of the experiment
filename_secondary = '/SaveToAvi-MJPG-secondary'
option_secondary = PySpin.MJPGOption()
option_secondary.frameRate = 60
option_secondary.quality = 75

#Open the recording file for both camera
avi_video_secondary.Open(filename_secondary, option_secondary)

while True:
    # Acquire an image(s)
    image = secondary_camera.GetNextImage()

    # Append to video
    avi_video_secondary.Append(image)

    # Pipe/Send image(s) back to the master process
    shared_queue.put(image)