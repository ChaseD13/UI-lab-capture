import os                                                                       
from multiprocessing import Pool, Queue                                               
                                                                                
                                                                                
processes = ('UI-lab-capture.py', 'Secondary_Camera_Control.py', 'Primary_Camera_Control.py')                                    
                                                  
                                                                                
def run_process(process):                                                             
    os.system('conda run {}'.format(process))                                       
                                                                                
shared_queue = Queue()                                                              
pool = Pool(processes=3)                                                        
pool.map(run_process, processes)   