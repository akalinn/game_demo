import key_event as ke
import time
import numpy as np

def check_caps():
    if ke.get_keybd_input('caps_lock'):
        print('Detect CAPS_LOCK key is on, program is ending...')
        return True
    return False

def main():
    ke.sleep(2)

    hwnd = ke.get_hwnd('MapleStory')
    if hwnd == 0:
        print("No Maplestory found in Process...")
        return -1
    ke.set_topwnd(hwnd)

    while not check_caps():

        ke.holdKey(['right_arrow'],(ke.rand()+0.5)/2+0.05)
        time.sleep(0.5)
        ke.holdKey(['left_arrow'],(ke.rand()+0.5)/2)
        time.sleep(0.5)
        ke.pressKey('a')
        ke.pressKey('a')
        ke.pressKey(' ')
        ke.sleep(1)




if __name__ == '__main__':
    main()
