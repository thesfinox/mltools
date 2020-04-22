import logging

from os import path, rename
from time import strftime, gmtime

def create_logfile(filename, name='logger', with_stdout=False, level=logging.INFO):
    '''
    Create a logfile and rotate old logs.
    
    Required arguments:
        filename:    the name of the file or path to the log.
        
    Optional arguments
        name:        the name of the log session,
        with_stdout: whether to output the log also on stdout,
        level:       the level of the information stored in the log.
        
    Returns:
        the log.
    '''
    
    # get current time to rename strings
    ctime = strftime('%Y%m%d.%H%M%S_', gmtime())
    
    # rotate log if it already exists
    if path.isfile(filename):
        print('Rotating existing logs...', flush=True)
        rename(filename, ctime + filename)
    
    # get a logging session by name
    log = logging.getLogger(name + ctime)
    log.setLevel(level)
    
    # define format
    fmt = logging.Formatter('%(asctime)s: %(levelname)s ==> %(message)s')
    
    # add the log file
    han = logging.FileHandler(filename=filename)
    han.setLevel(level)
    han.setFormatter(fmt)
    log.addHandler(han)
    
    # add handler for standard output
    if with_stdout:
        std = logging.StreamHandler(sys.stdout)
        std.setLevel(level)
        std.setFormatter(fmt)
        log.addHandler(std)
        
    return log
