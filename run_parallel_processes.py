import os                                                                       
from multiprocessing import Pool, Queue                                               
                                                                                
                                                                                
processes = ('UI-lab-capture.py', 'acquire_images.py', 'run_parallel_processes.py')                                    
                                                  
                                                                                
def run_process(process):                                                             
    os.system('conda run {}'.format(process))                                       
                                                                                
shared_queue = Queue()                                                              
pool = Pool(processes=3)                                                        
pool.map(run_process, processes)   