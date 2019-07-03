import sys
import numpy as np
import PySpin
import multiprocessing
from tkinter import messagebox


def run(queue, serial_number, running_experiment_queue):
    file = open('testfile_S_run.txt','w') 
    file.write('Hello World from SCC; In run! %d' % serial_number)
    file.close()


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
    filename_secondary = 'SaveToAvi-MJPG-secondary'
    option_secondary = PySpin.MJPGOption()
    option_secondary.frameRate = 60
    option_secondary.quality = 75

    #Open the recording file for both camera
    avi_video_secondary.Open(filename_secondary, option_secondary)

    while running_experiment_queue.empty():
        # Acquire an image(s)
        image = secondary_camera.GetNextImage()

        # Append to video
        avi_video_secondary.Append(image)

        # Pipe/Send image(s) back to the master process
        # Converts the grabbed image from ram into an Numpy array
        bimg = image.GetNDArray()
        queue.put(bimg)

    avi_video_secondary.Close()

    