#import time
from win32gui import GetWindowRect, GetForegroundWindow

def callback(hwnd,extra,rem_h,rem_w):
    rect = GetWindowRect(hwnd)
    print(rect)
    x = rect[0]+3
    y = rect[1]+26
    w = rect[2]-3-rem_w
    h = rect[3]-3-rem_h
    #print(str(w-x),' & ',str(h-y))
    return [x, y, w, h]

def locate(hwnd,rem_h,rem_w):
    #time.sleep(2)
    return callback(hwnd, None,rem_h,rem_w)

if __name__ == '__main__':
    locate(rem_h,rem_w)

