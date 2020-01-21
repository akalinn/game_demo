import key_event as ke
import time
import numpy as np

buff_key = ['alt','d','f','g','h','j','k']
cd = {'buff':150, 'b':8, 'F2':90, 'l':90, 'm':65}
record = {'buff':0, 'b':0, 'F2':0, 'l':0, 'm':0}

#250
def ult_driv(durantion,direction):
    ke.holdKey(['z',direction],durantion)

def ult_driv_stay(durantion):
    ke.holdKey(['z'],durantion)

#390
def twilight(times):
    t = times+int(ke.rand()*3)
    for i in range(0, t):
        ke.pressKey('x')

#250
def storm(durantion,direction):
    ke.sleep(ke.rand())
    ke.holdKey(['b',direction],durantion)
    record['b'] = time.time()

def cd_skill(key):
    ke.pressKey(key)
    record[key] = time.time()
    ke.sleep(1+ke.rand()/2)

def double_jump():
    ke.pressKey(' ')
    ke.pressKey(' ')
    ke.pressKey(' ')

def buff(keys):
    for key in keys:
        for i in range(0, int(ke.rand()*3+1)):
            ke.pressKey(key)

    record['buff'] = time.time()
    ke.sleep(1.5+ke.rand()/2)

def check_cd(key):
    if int(time.time() - record[key]) >= cd[key]:
        return True

    return False


def pattern1(direction, time):
    ke.sleep(0.5+ke.rand()/2)
    ult_driv(time,direction)

def pattern2(direction, times):
    ke.sleep(0.5+ke.rand()/2)
    if direction == 'right_arrow':
        direction = ['left_arrow']
    else:
        direction = ['right_arrow']

    ke.sleep((ke.rand()+1)/2)
    ke.holdKey(direction,(ke.rand()+0.7)/2)
    twilight(times)

def pattern3(direction):
    '''
    if ke.rand() < 0.5:
        pattern1(direction,6)
        if check_cd('m'):
            cd_skill('m')
            double_jump()
            ke.sleep((ke.rand()+1)/2)
            pattern1(direction,3)

        elif check_cd('b'):
            storm(6,direction)
        else:
            if ke.rand() < 0.5:
                ke.sleep((ke.rand()+1)/2)
                pattern1(direction,6)
            else:
                pattern2(direction, 8)    
    else:
        '''
    pattern2(direction, 10)
    if check_cd('b'):
        storm(6,direction)
    else:
        if ke.rand() < 0.5:
            ke.sleep((ke.rand()+1)/2)
            pattern1(direction,7)
        else:
            pattern2(direction, 10)         

def check_caps():
    if ke.get_keybd_input('caps_lock'):
        print('Detect CAPS_LOCK key is on, program is ending...')
        return True
    return False

def main():
    ke.sleep(2)

    #hwnd = ke.get_hwnd('MapleStory')
    obs_hwnd = ke.get_hwnd('obs64')
    if hwnd == 0:
        print("No Maplestory found in Process...")
        return -1
    #ke.set_topwnd(hwnd)
    if obs_hwnd == 0:
        print("No OBS found in Process...")
        return -1
    #ke.set_topwnd(hwnd)


    ke.holdKey(['right_arrow'],(ke.rand()+0.5)/2)



    while True:

        buff(buff_key)

        while not check_cd('buff'):
            if check_caps():
                return -1
    
            if ke.rand() < 0.05:
                hwnd = ke.get_hwnd('MapleStory')
                if hwnd == 0:
                    print("No Maplestory found in Process...")
                    return -1
                ke.set_topwnd(hwnd)


            cases = ['right_arrow','left_arrow']

            for direction in cases:
                if check_caps():
                    return -1
                r = ke.rand()
                if r < 0.8:
                    #print("2 ",end = '')
                    pattern2(direction,20)
                else:
                    #print("3 ",end = '')
                    pattern3(direction)
                #else:
                    #print("1 ",end = '')
                #    pattern1(direction,12)


    

if __name__ == '__main__':
    main()
