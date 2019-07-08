import sys
import numpy as np
import PySpin
import multiprocessing
from tkinter import messagebox
from PIL import Image, ImageTk


def run(queue, serial_number, running_experiment_queue, camera_fps):
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
    secondary_nodemap = secondary_camera.GetNodeMap()

    # Retrieve nodemap TLDevice
    secondary_nodemaptldevice = secondary_camera.GetTLDeviceNodeMap()

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

        # Append to video
        avi_video_secondary.Append(image)

        # Converts the grabbed image from ram into an Numpy array
        bimg = image.GetNDArray()

        # Pipe/Send image(s) back to the master process
        queue.put(bimg)

    avi_video_secondary.Close()

    