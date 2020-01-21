import win32pdh, string, win32api
import win32process
import win32process as process
import win32gui
import sys
from win32con import *


def procids():
    #each instance is a process, you can have multiple processes w/same name
    junk, instances = win32pdh.EnumObjectItems(None,None,'process', win32pdh.PERF_DETAIL_WIZARD)
    proc_ids=[]
    proc_dict={}
    for instance in instances:
        if instance in proc_dict:
            proc_dict[instance] = proc_dict[instance] + 1
        else:
            proc_dict[instance]=0
    for instance, max_instances in proc_dict.items():
        for inum in range(max_instances+1):
            hq = win32pdh.OpenQuery() # initializes the query handle 
            path = win32pdh.MakeCounterPath( (None,'process',instance, None, inum,'ID Process') )
            counter_handle=win32pdh.AddCounter(hq, path) 
            win32pdh.CollectQueryData(hq) #collects data for the counter 
            type, val = win32pdh.GetFormattedCounterValue(counter_handle, win32pdh.PDH_FMT_LONG)
            proc_ids.append((instance,str(val)))
            win32pdh.CloseQuery(hq) 

    proc_ids.sort()
    return proc_ids

def find_pid(Name):
    lists = procids()
    for process in lists:
        if process[0] == Name:
            return process[1]

    print('Does not find Process, Please check the Process Name!~')
    return -1



PORTABLE_APPLICATION_LOCATION = "F:\\Game\\MapleStory\\MapleStory.exe"



def callback(hwnd, procid):
    #if procid in  win32process.GetWindowThreadProcessId(hwnd):
    #    print("-----------------")
    #    return win32gui.SetForegroundWindow(hwnd)
    if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
        _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
        if found_pid == pid:
            hwnds.append(hwnd)
    return True


def show_window_by_process(procid):
    return win32gui.EnumWindows(callback, procid)


def runProgram(name):
    processHandler = find_pid(name)
    #don't run a process more than once
    if processHandler != -1:
        #Bring focus back to running window!
        print(processHandler)
        return show_window_by_process(processHandler)

    try:
        startObj = process.STARTUPINFO()
        myProcessTuple = process.CreateProcess(PORTABLE_APPLICATION_LOCATION,None,None,None,8,8,None,None,startObj)
        processHandler = myProcessTuple[2]
    except:
        print(sys.exc_info[0])


def get_hwnds(name):
    """return a list of window handlers based on it process id"""
    #def callback(hwnd, hwnds):
    #    if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
    #        _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
    #        if found_pid == pid:
    #            hwnds.append(hwnd)
    #    return True
    #hwnds = []
    #win32gui.EnumWindows(callback, hwnds)

    #print("Enumerated a total of windows with classes " ,(len(hwnds)))
    #return hwnds
    return win32gui.FindWindow(None, name)

def set_topwnd(hwnd):
    #win32gui.ShowWindow(hwnd,1)
    try:
        win32gui.SetForegroundWindow(hwnd)
    except pywintypes.error:
        pass