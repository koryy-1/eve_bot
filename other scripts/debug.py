import time
import datetime
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

hWnd = win32gui.FindWindow(None, 'EVE - AnSiri Senpai')

moveToX = 2240
moveToY = 250

gateCoordsX = 2204
gateCoordsY = 122
prosto_cnt = 0

XgridType1 = 2335
YgridType1 = 240
XgridType2 = 2448
YgridType2 = 650

Xgrid1 = 2122
Ygrid1 = 254 #240
Xgrid2 = 2150
Ygrid2 = 800

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
	# time.sleep(0.1)
	win32gui.PostMessage(hWnd, win32con.WM_MOUSEMOVE, None, lParam)
	time.sleep(0.1)
	win32gui.PostMessage(hWnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
	time.sleep(0.1)
	win32gui.PostMessage(hWnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, lParam)

def clickRB(x1,y1):
	lParam = win32api.MAKELONG(x1, y1)
	# while (win32api.GetKeyState(win32con.VK_CONTROL) < 0 or
	# 	   win32api.GetKeyState(win32con.VK_SHIFT) < 0 or
	# 	   win32api.GetKeyState(win32con.VK_MENU) < 0):
	# 	time.sleep(0.005)
	time.sleep(0.1)
	win32gui.PostMessage(hWnd, win32con.WM_MOUSEMOVE, None, lParam)
	time.sleep(0.1)
	win32gui.PostMessage(hWnd, win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON, lParam)
	time.sleep(0.1)
	win32gui.PostMessage(hWnd, win32con.WM_RBUTTONUP, win32con.MK_RBUTTON, lParam)



##############################################################################



### поиск окна по процессу

# def enum_window_callback(hwnd, pid):
#     tid, current_pid = win32process.GetWindowThreadProcessId(hwnd)
#     if pid == current_pid and win32gui.IsWindowVisible(hwnd):
#         windows.append(hwnd)

# # pid = 4416  # pid уже получен на предыдущем этапе
# windows = []

# qwe = win32gui.EnumWindows(enum_window_callback, 12624)
# # print(qwe)
# # Выводим заголовки всех полученных окон
# print([win32gui.GetWindowText(item) for item in windows])



# im = get_background_window(hWnd)
# im.save('LAST_SCREENSHOT.jpg')


# img = cv2.imread('LAST_SCREENSHOT.jpg')

def find_targets():
	im = get_background_window(hWnd)
	image_grid_row = im.crop( (Xgrid1, Ygrid1-23, Xgrid2, Ygrid2-23) )

	img_array = np.asarray(image_grid_row)

	bgr_for_hsv = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)

	cat_hsv = cv2.cvtColor(bgr_for_hsv, cv2.COLOR_BGR2HSV)
	cat_color_low_red = (0,155,84) #более красный ненасыщенный
	cat_color_high_red = (15,255,255) #темно красный
	only_cat_hsv = cv2.inRange(cat_hsv, cat_color_low_red, cat_color_high_red)

	# calculate moments of binary image
	M = cv2.moments(only_cat_hsv)
	if (M["m00"] != 0):
		print('enemy added')
		return True
	else:
		print('enemy NOT added')
		return False

def something():
	for i in range(5):
		# image = Image.open('Screenshot_18.png')
		image = get_background_window(hWnd)

		image1 = image.crop( (1000, 450, 1560, 970) )
		img_arr = np.asarray(image1)
		img_arr = cv2.cvtColor(img_arr, cv2.COLOR_BGR2RGB)

		img_hsv = cv2.cvtColor(img_arr, cv2.COLOR_BGR2HSV)
		img_hsv_low_red = (0,155,84) #более красный ненасыщенный
		img_hsv_high_red = (15,255,255) #темно красный
		img_hsv_red = cv2.inRange(img_hsv, img_hsv_low_red, img_hsv_high_red)

		imgGrey = cv2.cvtColor(img_arr, cv2.COLOR_BGR2GRAY)
		_, thrash = cv2.threshold(img_hsv_red, 240, 255, cv2.THRESH_BINARY)
		contours, _ = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)


		for contour in contours:
			approx = cv2.approxPolyDP(contour, 0.05 * cv2.arcLength(contour, True), True)
			x = approx.ravel()[0]
			y = approx.ravel()[1]
			if (len(approx) == 3):
				
				# x1 = approx.ravel()[0]
				# y1 = approx.ravel()[1]
				# x2 = approx.ravel()[2]
				# y2 = approx.ravel()[3]
				# x3 = approx.ravel()[4]
				# y3 = approx.ravel()[5]
				# print(y1, y2, '    ', x2, x3)
				# if (y2 - y1 == 3 and x3 - x1 == 5):

				# print(x1, y1, x2, y2, x3, y3)
				# print('approx', approx)
				# cv2.circle(img_arr, (x, y), 5, (255, 255, 255), -1)
				# cv2.putText(img_arr, 'triangle', (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255))
				break

		clickRB(x+1000, y+450)
		time.sleep(0.5)
		clickLB(x+5 + 1000+60, y+5 + 450+165)
		time.sleep(1)
		if find_targets:
			break

	# cv2.imshow('shape', img_arr)
	# # cv2.imshow('sample', imgGrey)
	# cv2.imshow('red', img_hsv_red)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()



def find_word(string):
	x, y, w, h = 0, 0, 0, 0

	im = get_background_window(hWnd)
	image = im.crop( (870, 415-23, 985, 440-23) )
	image = np.asarray(image)

	# Будет выведен весь текст с картинки
	config = r'--oem 3 --psm 6'

	# Делаем нечто более крутое!!!

	data = pytesseract.image_to_data(image, config=config)

	# Перебираем данные про текстовые надписи
	for i, el in enumerate(data.splitlines()):
		if i == 0:
			continue

		el = el.split()
		try:
			if(
				(fuzz.token_set_ratio(el[11], string)) > 50
			):
				x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])
				break
		except IndexError:
			pass
			# print("Операция была пропущена")

	if (y != 0):
		print(f'{string} detected')
		y = y+int(h/2)
		return y
	print(f'{string} NOT detected')
	return False

def check_sec():
	im = get_background_window(hWnd)
	image_grid_row = im.crop( (1200, 585-23, 1380, 610-23) )

	img_array = np.asarray(image_grid_row)

	bgr_for_hsv = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)

	cat_hsv = cv2.cvtColor(bgr_for_hsv, cv2.COLOR_BGR2HSV)
	cat_color_low_red = (0,155,84) #более красный ненасыщенный
	cat_color_high_red = (20,255,255) #темно красный
	only_cat_hsv = cv2.inRange(cat_hsv, cat_color_low_red, cat_color_high_red)

	# calculate moments of binary image
	M = cv2.moments(only_cat_hsv)


	if (M["m00"] != 0):
		print('low or null sec')
	else:
		print('high sec')
		return True


def find_exp():
	clickLB(20, 135-23)
	time.sleep(1)
	clickLB(850, 1023-23)
	time.sleep(1)
	if find_word('ESCALATIONS'):
		x = 1100
		y = 535
		while y <= 400+535:
			clickLB(x, y-23)
			y += 100
			time.sleep(0.5)
			if check_sec():
				clickLB(1550, 933-23)
				time.sleep(1)
				clickLB(20, 135-23)
				time.sleep(2)
				return True
		
	clickLB(20, 135-23)
	return False

def lay_route():
	x = 1845
	y = 660
	
	for i in range(8):
		x = 1845
		for j in range(3):
			clickRB(x, y-23)
			time.sleep(0.2)
			clickLB(x+60, y+60-23)
			time.sleep(0.2)
			x += 85
		y += 16
# lay_route()

def qwe(x,y=3, sad='qwe'):
	print(x, y, sad)

qwe(5)