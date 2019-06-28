# This script will init and collect images from both the primary and secondary cameras
import sys
import PySpin

camera_list = [sys.argv[1], sys.argv[2]]
queue = [sys.argv[3], sys.argv[4]]

for i in range(2):
    image = camera_list[i].GetNextImage()
    queue[i].put(image)
    # Display image to preview


