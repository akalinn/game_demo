import win32com.client,time
import win

def simple():



	time.sleep(2)
	#hwnd = win.get_hwnds("MapleStory")
	#win.set_topwnd(hwnd)

	shell = win32com.client.Dispatch("WScript.Shell")
	#shell.AppActivate("MapleStory")

	hwnd = win.get_hwnds("MapleStory")
	#win.set_topwnd(hwnd)


	now = time.time()
	while (time.time()-now < 2):

		shell.sendKeys("3")
		time.sleep(0.2)
		#win32api.PostMessage(hwnd,win32con.WM_CHAR,65,0) #释放按键
		

	#from ctypes import *
	#import timeaaa

	#sc = windll.user32.MapVirtualKey(0x41, 0)
	#print(sc)


if __name__ == '__main__':
    simple()

