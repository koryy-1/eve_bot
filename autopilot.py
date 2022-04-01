import time
import cv2
from PIL import Image, ImageGrab
import numpy as np
import pyautogui
import pytesseract
import win32api
import win32con
import win32gui
import win32ui
import win32process
from ctypes import windll

from fuzzywuzzy import fuzz

moveToX = 2240
moveToY = 245

gateCoordsX = 2204
gateCoordsY = 122
prosto_cnt = 0

hWnd = win32gui.FindWindow(None, 'EVE - AnSiri Senpai')

def get_background_window(hwnd):
	left, top, right, bot = win32gui.GetWindowRect(hwnd)
	w = right - left
	h = bot - top

	hwndDC = win32gui.GetWindowDC(hwnd)
	mfcDC = win32ui.CreateDCFromHandle(hwndDC)
	saveDC = mfcDC.CreateCompatibleDC()

	saveBitMap = win32ui.CreateBitmap()
	saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

	saveDC.SelectObject(saveBitMap)

	result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)

	bmp_info = saveBitMap.GetInfo()
	bmp_str = saveBitMap.GetBitmapBits(True)

	im = Image.frombuffer(
	    'RGB',
	    (bmp_info['bmWidth'], bmp_info['bmHeight']),
	    bmp_str, 'raw', 'BGRX', 0, 1)

	win32gui.DeleteObject(saveBitMap.GetHandle())
	saveDC.DeleteDC()
	mfcDC.DeleteDC()
	win32gui.ReleaseDC(hwnd, hwndDC)

	if result == 1:
	    return im

def clickLB(x1,y1):
	lParam = win32api.MAKELONG(x1, y1)
	while (win32api.GetKeyState(win32con.VK_CONTROL) < 0 or
		   win32api.GetKeyState(win32con.VK_SHIFT) < 0 or
		   win32api.GetKeyState(win32con.VK_MENU) < 0):
		time.sleep(0.005)
	time.sleep(0.1)
	win32gui.PostMessage(hWnd, win32con.WM_MOUSEMOVE, None, lParam)
	time.sleep(0.1)
	win32gui.PostMessage(hWnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
	time.sleep(0.1)
	win32gui.PostMessage(hWnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, lParam)

# x, y = pyautogui.position()
# print(x, y)

# image.show()


### прыг в следующую систему
def go_next():
	global moveToX
	global moveToY

	global gateCoordsX
	global gateCoordsY
	global prosto_cnt
	im = get_background_window(hWnd)
	image_grid_row = im.crop( (2122, 240-23, 2150, 500-23) )

	img_array = np.asarray(image_grid_row)

	bgr_for_hsv = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)

	cat_hsv = cv2.cvtColor(bgr_for_hsv, cv2.COLOR_BGR2HSV) #Преобразуем в HSV
	cat_color_low_yellow = (25,180,150) #более желтый ненасыщенный
	cat_color_high_yellow = (35,255,255) #темно желтый
	only_cat_hsv_yellow = cv2.inRange(cat_hsv, cat_color_low_yellow, cat_color_high_yellow)

	# calculate moments of binary image
	M_yellow = cv2.moments(only_cat_hsv_yellow)

	if(M_yellow["m00"] == 0):
		if(prosto_cnt < 1):
			prosto_cnt += 1
			time.sleep(8)
			return
		print('корабль прошел маршрут')
		exit(0)
	else:
		prosto_cnt = 0

	# x, y = pyautogui.position()

	# if((x == 2204) and (y == 122)):
	# 	pyautogui.click()
	# else:
	# 	pyautogui.moveTo(moveToX, moveToY)
	# 	pyautogui.click()
	# 	time.sleep(0.25)

	# 	pyautogui.moveTo(gateCoordsX, gateCoordsY)
	# 	pyautogui.click()


	clickLB(moveToX, moveToY-23)
	time.sleep(0.2)
	clickLB(gateCoordsX, gateCoordsY-23)


### проверка находится ли корабль в варпе
def check_state(sec):
	time.sleep(4)
	tryes = 0
	while True:
		im = get_background_window(hWnd)
		img_state = im.crop( (1120, 1050-23, 1450, 1190-23) )

		img_state_string = np.asarray(img_state)

		rgb_state = cv2.cvtColor(img_state_string, cv2.COLOR_BGR2RGB)


		psm4_state = pytesseract.image_to_string(rgb_state, config='--psm 4')
		psm6_state = pytesseract.image_to_string(rgb_state, config='--psm 6')
		if(
			(fuzz.token_set_ratio(psm4_state, 'WARP')) > 50
			or
			(fuzz.token_set_ratio(psm6_state, 'WARP')) > 50
		):
			if(tryes > 12):
				print('произошел вылет из игры')
				exit(0)
			tryes += 1
			print('ship still warping...')
			time.sleep(sec)
		else:
			print('ship finished warping')
			if(sec == 10):
				time.sleep(2.5)
				im = get_background_window(hWnd)
				img_state = im.crop( (1120, 1050-23, 1450, 1190-23) )

				img_state_string = np.asarray(img_state)

				rgb_state = cv2.cvtColor(img_state_string, cv2.COLOR_BGR2RGB)


				psm4_state = pytesseract.image_to_string(rgb_state, config='--psm 4')
				psm6_state = pytesseract.image_to_string(rgb_state, config='--psm 6')
				if(
					(fuzz.token_set_ratio(psm4_state, 'JUMP')) > 50
					or
					(fuzz.token_set_ratio(psm6_state, 'JUMP')) > 50
				):
					print('ship still jumping...')
					time.sleep(5)
					continue
				else:
					print('ship finished jumping')
					time.sleep(3)
			break

while True:
	go_next()
	check_state(10)