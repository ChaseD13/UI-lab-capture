import sys
from tkinter import messagebox, Tk
import time

def run(running_experiment_queue, counter):
    # Increment shared total seconds
    while running_experiment_queue.empty():
        counter.value += 1
        time.sleep(1)