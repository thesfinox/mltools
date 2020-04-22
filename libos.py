import os
import psutil

class InfoOS:
    '''
    This class retrieves and prints information on the current OS.
    
    Public methods:
    
    Attributes:
        os:      the current OS,
        kernel:  the current release,
        arch:    the current architecture,
        threads: the number of available CPU threads,
        freq:    the current CPU frequency,
        freqm:   the maximum CPU frequency,
        vmtot:   the total virtual memory (in MB),
        vmav:    the available virtual memory (in MB).
    '''
    
    def __init__(self):
        '''
        Constructor of the class.
        '''
        
        self.os      = os.uname().sysname
        self.kernel  = os.uname().release
        self.arch    = os.uname().machine
        self.threads = psutil.cpu_count()
        self.freq    = psutil.cpu_freq().current
        self.freqm   = psutil.cpu_freq().max
        self.vmtot   = int(psutil.virtual_memory().total / 1024 / 1024)
        self.vmav    = int(psutil.virtual_memory().available / 1024 / 1024)
