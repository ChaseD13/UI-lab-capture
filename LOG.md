# LOG 

### 5/29
- Introduction to the lab equipment
- **SpinView** was able to see an image trhough the **FLIR** camera
- **LJControlPanel** was able to find and read values from the **Labjack U3-LV**

### 5/30
- Installed Anaconda
  - Imported tkinter and labjack 
- **Labjack** is reading voltage that is being sent from an Arduino board
- *Suggestion:* Be able to adjust the scale of the reads from the labjack 
- *Idea:* Be able to add more inputs via the GUI 
- Added an entry field to the GUI

### 5/31
- Added a Active Directory/Settings page that is prompted on open
- Added graph to track the incoming analog input
- Changed the entry field to a slider to increase/decrease the scan Hz
- Installed **PySpin** using the **Spinnaker SDK**

### 6/3
- Added multiple AIN inputs for all eight ports
- Edited the functionality of the slider. It now works in Hz 
- Added File I/O to store data to the location of the AD set by the user
- Added frames to the layout to try and make positioning elements easier

### 6/4
- Added functionality to take a photo using one **FLIR Blackfly S** camera
- Added structure to support the Primary/Secondary system for capturing video
- Added the ability to access the amplitude from the labjack in a stream 
- Added a Start/Stop experiment button for better control

### 6/5
- Corrected functionality for the start/stop buttons
  - they now tart and stop the experiment properly
- Hz is now back to an entry. The experiment should have a set hz once the scientist hits start
