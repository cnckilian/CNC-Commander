#!/usr/bin/env python3

import sys, os
import re
from datetime import datetime
from time import time


# ==============================================================================
# Main program function
# ------------------------------------------------------------------------------

def main():
    
    print("CNC-Commander V0.1")
    
    new_entry = []
    start = 0
    end = 0
    directory = ""
    project = ""
    usage_type = "?"
    person = "?"
    path_bbctrllog='/var/log/bbctrl.log'
    path_userlog='/home/bbmc/cnc-commander/user.log'
    path_bbctrllog='data/bbctrl.log'
    path_userlog='data/user.log'
    
    # While-loop to catch the situation of renamed log files
    while True:
        try:
            # Loop over the tailing entries in the log file
            for new_entry in tail_logfile(path_bbctrllog):
                try:
                    if new_entry[:5] == 'USER:':
                        _, person, usage_type = new_entry.split()
                    elif (new_entry[:25] == "I:Planner:GCode:./upload/"):
                        project = new_entry[25:-4]
                    elif (new_entry[:21] == 'I:Planner:Program End' or new_entry[:21] == 'I:Planner:Program Sto'):
                        #Get the time
                        end = datetime.strptime(new_entry[-26:-7],'%Y-%m-%dT%H:%M:%S').timestamp()
                        if (start != 0):
                            #Calculate difference
                            milling_time = round((end - start)/60,1)
                            start = 0
                            f=open(path_userlog,'a+')
                            #Save Time: type of usage_type / person / milling time / project / Date to user.log
                            print(usage_type + "\t" + person + "\t" + str(milling_time).replace(".",",") + "\t" + project + "\t" + datetime.strptime(new_entry[-26:-7],'%Y-%m-%dT%H:%M:%S').isoformat()[0:10])
                            f.write(usage_type + "\t" + person + "\t" + str(milling_time).replace(".",",") + "\t" + project + "\t" + datetime.strptime(new_entry[-26:-7],'%Y-%m-%dT%H:%M:%S').isoformat()[0:10] + "\n")
                            f.close()
                    elif (new_entry[:21] == 'I:Planner:Program Sta'):
                        #Get the times
                        start = datetime.strptime(new_entry[-26:-7],'%Y-%m-%dT%H:%M:%S').timestamp()
                except Exception as e:
                    #f=open("/home/bbmc/cnc-commander/user.log",'a+')
                    print(e)
                    #f.write(str(e))
                    #f.close()
        except FileNotFoundError:
            # This is the case after the logfile was renamed to log.1 ad just 
            # before the new log file is created.
            pass


# ==============================================================================
# Helper functions
# ------------------------------------------------------------------------------

def tail_logfile( path, method='pythonic', break_when_smaller=True ):
    '''
    Methods for tailing a (log) file.
    Usage: 
        ```
        for line in tail_logfile(...):
            print(line)
        ```
     - with break_when_smaller=True, the iterator is stopped when the file size 
       has become smaller than the initial size. This can be the case when the
       actually tailed file was renamed and a new file was created. 
    '''
    
    if break_when_smaller:
        initial_filesize = os.path.getsize(path)
    
    if method == 'tailer':
        # ---------------------------------------------------------
        # Method based on module tailer
        # ---------------------------------------------------------
        import tailer
        for line in tailer.follow(open(path, 'r')):
            if break_when_smaller and (os.path.getsize(path) < initial_filesize):
                break
            yield line
    
    elif method == 'pythonic':
        # ---------------------------------------------------------
        # pythonic implementation
        # ---------------------------------------------------------
        from time import sleep
        logfile = open(path,'r')
        logfile.readlines()
        while True:
            if break_when_smaller and (os.path.getsize(path) < initial_filesize):
                break
            line = logfile.readline()
            if line.strip() is '':
                sleep(0.1)
                continue
            yield line.strip()
    else:
        raise NotImplementedError
    return


# ==============================================================================
# invoke main program function
# ------------------------------------------------------------------------------

if __name__ == '__main__':
    sys.exit(main())
