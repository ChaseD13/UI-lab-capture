import sys
import numpy as np
import PySpin
import multiprocessing
from tkinter import messagebox


def run(queue, serial_number, running_experiment_queue):
    file = open('testfile_P_run.txt','w') 
    file.write('Hello World from PCC; In run! %d' % serial_number)
    file.close()


    # Get system
    system = PySpin.System.GetInstance()
    # Get camera list
    cam_list = system.GetCameras()
    # Figure out which is primary and secondary
    if cam_list.GetByIndex(0).TLDevice.DeviceSerialNumber() == str(serial_number):
        primary_camera = cam_list.GetByIndex(0)
    else:
        primary_camera = cam_list.GetByIndex(1)
        
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
    filename_primary = 'SaveToAvi-MJPG-primary'
    option_primary = PySpin.MJPGOption()
    option_primary.frameRate = 60
    option_primary.quality = 75

    #Open the recording file for both camera
    avi_video_primary.Open(filename_primary, option_primary)

    while running_experiment_queue.empty():
        # Acquire an image(s)
        image = primary_camera.GetNextImage()

        # Append to video
        avi_video_primary.Append(image)

        # Pipe/Send image(s) back to the master process
        # Converts the grabbed image from ram into an Numpy array
        bimg = image.GetNDArray()
        queue.put(bimg)

    avi_video_primary.Close()

    