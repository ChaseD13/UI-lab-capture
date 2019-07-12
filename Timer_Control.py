from tkinter import messagebox, Tk
import sys
import time


# Timer that increments every second and passes result back to master
def run(running_experiment_queue, counter):
        # Increment shared total seconds
        while running_experiment_queue.empty():
                counter.value += 1
                time.sleep(1)
        