import pyautogui, time, os
from tkinter import *

#List to hold values from the set up window
values = []

#Returns a tuple represint the coordinates of the mouse's current position on the screen
def getMousePosition():
    x, y = pyautogui.position()
    return x , y


#Startup window to set desired settings
def promptWindow():
    master = Tk()

    Label(master, text = "Enter # of channels:").pack()
    chn = Entry(master)
    chn.pack()

    Label(master, text = "Enter scan hz:").pack()
    scn = Entry(master)
    scn.pack()

    chn.focus_set()

    def submit():
        values.append(chn.get())
        values.append(scn.get())
        master.destroy()

    b = Button(master, text = 'Ok', width = 10, command = submit)
    b.pack()

    mainloop()
    

def main():
    #Enable the fail safe, triggered by moving the mouse to the upper left of the screen
    pyautogui.FAILSAFE = True

    try:
        promptWindow()

        numChannels = values[0]
        scanHz = values[1]

        #Opens LJStramUD
        #NOTE: On color for graph button is (105, 254, 33)
        os.startfile(r'C:\Program Files (x86)\LabJack\Applications\LJStreamUD.exe')

        time.sleep(1)

        pyautogui.moveTo(873, 115, duration= 2)

        for i in range(int(numChannels)):
            w, h = getMousePosition()

            if not pyautogui.pixelMatchesColor(w, h, (124, 254, 56)):
                pyautogui.click(w, h, button= 'left')

            if i != (int(numChannels) - 1):
                pyautogui.moveRel(0 , 25, duration= .5)
        

        #Sets the number of channels
        pyautogui.moveTo(50, 116, duration= 1)
        time.sleep(2)
        w, h = getMousePosition()
        pyautogui.doubleClick(w, h)
        pyautogui.typewrite(numChannels)

        #Sets the scan hz 
        pyautogui.moveTo(50, 160, duration= 1)
        w,h = getMousePosition()
        pyautogui.doubleClick(w, h)
        pyautogui.typewrite(scanHz)

        #Starts the stream
        pyautogui.moveTo(80, 380, duration= 1)
        w,h = getMousePosition()
        pyautogui.click(w, h, button= 'left')

        #Break
        time.sleep(10)

        #Opens the SpinView Program
        os.startfile(r'C:\Program Files (x86)\Point Grey Research\Spinnaker\bin\vs2015\SpinView_WPF.exe')

        #Move the mouse, select the first camera
        pyautogui.moveTo(664,317, duration = 1)
        time.sleep(4)
        w , h = getMousePosition()
        pyautogui.doubleClick(w, h)

        #Move the mouse, select the play button
        pyautogui.moveTo(962, 255, duration= 1)
        time.sleep(5)
        w, h = getMousePosition()
        pyautogui.click(w, h, button= 'left')


    except KeyboardInterrupt:
        print("Keyboard Interupt Handled")
        return 
    
    except pyautogui.FailSafeException:
        print("Fail Safe Exception Handled")
        return 
    
    print("Finished...")

if __name__ == "__main__":
    main()