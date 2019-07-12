from PIL import Image, ImageTk
from tkinter import messagebox
import multiprocessing
import numpy as np
import PySpin
import sys


# Handles initialization, recording captured images, frame verification, and passing images back to master via numpy array
def run(queue, serial_number, running_experiment_queue, camera_fps, preview_queue, missed_frames):
    # Starting frame number
    starting_frame = 0

    counter = 0

    # Previous frame number
    previous_frame = 0

    # First iteration 
    first_iteration = True

    # Write Logisitcs out to Log file
    output_file = open('Frames_Secondary.dat', "a+")

    # Get system
    system = PySpin.System.GetInstance()
    # Get camera list
    cam_list = system.GetCameras()
    # Figure out which is primary and secondary
    if cam_list.GetByIndex(0).TLDevice.DeviceSerialNumber() == str(serial_number):
        secondary_camera = cam_list.GetByIndex(0)
    else:
        secondary_camera = cam_list.GetByIndex(1)

    # Init Camera
    secondary_camera.Init()

    # Retrieve GenICam nodemap
    # secondary_nodemap = secondary_camera.GetNodeMap()

    # Retrieve nodemap TLDevice
    # secondary_nodemaptldevice = secondary_camera.GetTLDeviceNodeMap()

    # Setup the hardware triggers
    # NOTE: Turned off for now because gpio pins not connected
    secondary_camera.TriggerMode.SetValue(PySpin.TriggerMode_Off)

    # Set up secondary camera trigger
    # secondary_camera.TriggerSource.SetValue(PySpin.TriggerSource_Line3)
    # secondary_camera.TriggerOverlap.SetValue(PySpin.TriggerOverlap_ReadOut)
    # secondary_camera.TriggerMode.SetValue(PySpin.TriggerMode_On)# # Set up primary camera trigger


    # Set acquisition mode
    secondary_camera.AcquisitionMode.SetValue(PySpin.AcquisitionMode_Continuous)
    
    # Set aquisition rate to desired fps for both cameras
    #TODO: Make this argument changeable
    secondary_camera.AcquisitionFrameRateEnable.SetValue(True)
    secondary_camera.AcquisitionFrameRate.SetValue(camera_fps.value)

    secondary_camera.BeginAcquisition()

    #Start the video

    #Create a SpinVideo instance for both cameras
    avi_video_secondary = PySpin.SpinVideo()

    #Set filename and options for both videos
    #TODO: Make the video path save to the working directory of the experiment
    filename_secondary = 'SaveToAvi-MJPG-secondary'
    option_secondary = PySpin.MJPGOption()
    option_secondary.frameRate = camera_fps.value
    option_secondary.quality = 75

    #Open the recording file for both camera
    avi_video_secondary.Open(filename_secondary, option_secondary)

    while running_experiment_queue.empty():
        # Acquire an image(s)
        image = secondary_camera.GetNextImage()

        if first_iteration:
            first_iteration = False
            starting_frame = image.GetFrameID()
            previous_frame = starting_frame - 1

        # Check if running experiment
        if not preview_queue.empty():
            # Append to video
            avi_video_secondary.Append(image)

             # Check for missed frame
            if image.GetFrameID() != previous_frame + 1:
                missed_frames.value += 1
                output_file.write('~~~~~~~~ MISSED FRAME HERE ~~~~~~~~ FID_%d :: PFID_%d :: PFID+1_%d\n' % (image.GetFrameID(), previous_frame, previous_frame + 1)) 
        previous_frame = image.GetFrameID()

        # Converts the grabbed image from ram into an Numpy array
        bimg = image.GetNDArray()

        # Pipe/Send image(s) back to the master process
        counter += 1
        if counter%4 == 0:
            queue.put(bimg)

        output_file.write('%d\n' % image.GetFrameID()) 

        # Remove image from the camera buffer
        image.Release()

    output_file.close()
    avi_video_secondary.Close()
    secondary_camera.EndAcquisition()
    secondary_camera.DeInit()
    del secondary_camera
    del cam_list
    del system
