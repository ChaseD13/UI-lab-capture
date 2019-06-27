import os                                                                       
from multiprocessing import Pool                                                
                                                                                
                                                                                
processes = ('UI-lab-capture.py')##, 'process2.py', 'process3.py')                                    
                                                  
                                                                                
def run_process(process):                                                             
    os.system('conda run {}'.format(process))                                       
                                                                                
                                                                                
pool = Pool(processes=1)                                                        
pool.map(run_process, processes)   