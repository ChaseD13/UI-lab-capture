# This script will append collected images to MPJG video
import sys
import PySpin

queue = [sys.argv[1], sys.argv[2]]
video = [sys.argv[3], sys.argv[4]]

for i in range(2):
    image = queue[i].get()
    video[i].Append(image)