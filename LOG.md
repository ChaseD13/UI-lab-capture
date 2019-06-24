# LOG 

### 5/29
- Introduction to the lab equipment
- **SpinView** was able to see an image trhough the **FLIR Blackfly S** camera
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
- Primary camera can now take an image and display it on the GUI

### 6/6
- Added graph that pulls data from the **Labjack U3-LV** via a stream
  - Displays all 8 analog channels
- Redesigned GUI using pack instead of grid
- Added more entry options for data aquisition 
- Stop button erases figure but keeps graph
- Added starting framework for editing the number of channels visible

### 6/7
- Out of Office

### 6/10
- Added ability to record a video of specified frames from the **Blackfly S** camera
  - Capturing at 60hz

### 6/11
- Added an entry for the number of channels
- Added decent functionality towards aquring video from the cameras

### 6/12 
- Added framework for multithreading
- Reliably capture 60hz video composed of 1000 images
- Created a GUIA which preforms the order of operations using the mouse, keyboard, and software applications

### 6/13 
- Added class to handle recording/capturing frames

### 6/14
- Reformated code
- Threading succesfully saves avi video at 15fps 

### 6/17
- Added simultaneous streaming for two **FLIR Blackfly S** cameras
- Reliable recording @60 fps
- Added lost frame tracking using FrameID's

### 6/18
- Changed frame dropped counter; Now increments based on difference between to non-sequential frames
- Changed how data stream from **Labjack U3-LV** is exported
- Added variable to set both cameras FPS 

### 6/19
- Added time scaling to the output file
- Reformated how data is exported from the labjack
- Each camera owns two threads; One aquires frames, the other appends them to the avi video

### 6/20
- Added entry to make hz between camera and labjack more clear
- Frame id's are now added to a queue and exported into Additional docs
- Data and cameras now return expected results :^)

### 6/21 
- Camera preview!