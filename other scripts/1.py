import win32api
import win32gui
import win32ui
import time

time.sleep(3)
hWnd_manual = win32gui.GetForegroundWindow()
hWnd = win32gui.FindWindow(None, 'EVE - AnSiri Senpai')
print('manual', hWnd_manual, '\nauto', hWnd) # 105711036