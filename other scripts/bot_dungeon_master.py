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
# 2560 * 1080

gateCoordsX = 2204
gateCoordsY = 122

# 1 vkladka
X1vkladka = 2272 #2180
Y1vkladka = 215 #204

# 3 vkladka
X3vkladka = 2370 #2300
Y3vkladka = 215

Xgrid1 = 2122
Ygrid1 = 254 #240
Xgrid2 = 2150
Ygrid2 = 800

XgridType1 = 2220 #2335
YgridType1 = 254 #240
XgridType2 = 2335 #2448
YgridType2 = 650

XdroneMod1 = 1884
YdroneMod1 = 925
XdroneMod2 = 2032
YdroneMod2 = 1032

XdroneHP1 = 2085
YdroneHP1 = 925
XdroneHP2 = 2097
YdroneHP2 = 1025

# approach_state
XmiddleText1 = 1120
YmiddleText1 = 1050
XmiddleText2 = 1450
YmiddleText2 = 1190

# max vel
XmaxVel = 1325
YmaxVel = 1333

# ship stop
X0Vel = 1232
Y0Vel = 1333

# 1400 m/s
XconstVel = 1286
YconstVel = 1355

# take all
XtakeAllBtnCoords = 256
YtakeAllBtnCoords = 990

XopenedCont1 = 120
YopenedCont1 = 570
XopenedCont2 = 176
YopenedCont2 = 590

# for sort
XwndSpace = 774
YwndSpace = 696

XactivateFilament = 1154
YactivateFilament = 870

XEnterToDange = 1275
YEnterToDange = 840

XcargoInd1 = 346
YcargoInd1 = 500
XcargoInd2 = 357
YcargoInd2 = 513

XbtnUndock1 = 2340
YbtnUndock1 = 190
XbtnUndock2 = 2500
YbtnUndock2 = 230

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
	# while (win32api.GetKeyState(win32con.VK_CONTROL) < 0 or
	# 	   win32api.GetKeyState(win32con.VK_SHIFT) < 0 or
	# 	   win32api.GetKeyState(win32con.VK_MENU) < 0):
	# 	time.sleep(0.005)
	time.sleep(0.1)
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


def press_btn(BTN):
	# while (win32api.GetKeyState(win32con.VK_CONTROL) < 0 or
	# 		win32api.GetKeyState(win32con.VK_SHIFT) < 0 or
	# 		win32api.GetKeyState(win32con.VK_MENU) < 0
	# 	):
		# time.sleep(0.005)
	temp = win32gui.PostMessage(hWnd, win32con.WM_IME_KEYDOWN, BTN, 0)
	time.sleep(0.05)
	temp = win32gui.PostMessage(hWnd, win32con.WM_IME_KEYUP, BTN, 0)
	time.sleep(0.1)

def lock_target(Y):
	lParam1 = win32api.MAKELONG(Xgrid2+100, Ygrid1+Y-23)
	lParam2 = win32api.MAKELONG(Xgrid2-100, Ygrid1+Y-23)
	# while (win32api.GetKeyState(win32con.VK_CONTROL) < 0 or
	# 		win32api.GetKeyState(win32con.VK_SHIFT) < 0 or
	# 		win32api.GetKeyState(win32con.VK_MENU) < 0
	# 	):
		# time.sleep(0.005)
	time.sleep(0.1)
	win32gui.PostMessage(hWnd, win32con.WM_MOUSEMOVE, None, lParam1)
	time.sleep(0.1)
	win32gui.PostMessage(hWnd, win32con.WM_KEYDOWN, win32con.VK_CONTROL, 0)
	time.sleep(0.2)
	win32gui.PostMessage(hWnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam1)
	time.sleep(0.1)
	win32gui.PostMessage(hWnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, lParam1)
	time.sleep(0.1)
	win32gui.PostMessage(hWnd, win32con.WM_KEYUP, win32con.VK_CONTROL, 0)
	time.sleep(0.1)

	win32gui.PostMessage(hWnd, win32con.WM_MOUSEMOVE, None, lParam2)
	time.sleep(0.1)

def check_drones_quantity():
	im = get_background_window(hWnd)
	image = im.crop( (1980, 857-23, 2000, 874-23) )
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
			# print(el[11])
			# print(fuzz.token_set_ratio(el[11], '8'))
			# print(fuzz.token_set_ratio(el[11], '()'))
			# print(fuzz.token_set_ratio(el[11], '2'))
			if(
				el[11] == '()'
				or
				(fuzz.token_set_ratio(el[11], '8')) > 50
				or
				(fuzz.token_set_ratio(el[11], '()')) > 50
				or
				(fuzz.token_set_ratio(el[11], '2')) > 50
			):
				print('not enough drone')
				exit(0)
		except IndexError:
			pass
			# print("Операция была пропущена")

def check_cargo():
	im = get_background_window(hWnd)
	image_drones = im.crop( (XcargoInd1, YcargoInd1-23, XcargoInd2, YcargoInd2-23) )

	img_array_dr = np.asarray(image_drones)

	bgr_for_hsv = cv2.cvtColor(img_array_dr, cv2.COLOR_BGR2RGB)

	cat_hsv = cv2.cvtColor(bgr_for_hsv, cv2.COLOR_BGR2HSV) #Преобразуем в HSV

	cat_color_low_red = (80,175,40) #более синий ненасыщенный
	cat_color_high_red = (255,255,255) #темно синий
	only_cat_hsv_red = cv2.inRange(cat_hsv, cat_color_low_red, cat_color_high_red)

	# calculate moments of binary image
	M_blue = cv2.moments(only_cat_hsv_red)

	if(M_blue["m00"] != 0):
		print('full cargo')
		return True
	else:
		return False

def unload_cargo():
	statY = find_station()
	if (statY):
		clickLB(Xgrid2, Ygrid1+statY-23)
		time.sleep(1)
		clickLB(gateCoordsX, gateCoordsY-23)
	else:
		exit(0)
	time.sleep(20) #20

	find_bnt_undock()
	for i in range(3):
		clickRB(XwndSpace, YwndSpace)
		time.sleep(0.2)
		clickLB(XwndSpace+50, YwndSpace+70) # sort
		time.sleep(2)
		x, y = find_filament()
		if (y != 0):
			break
		if (i == 2):
			print('no calm exotic')
			exit(0)
		print('bad try to find filament')
	clickRB(x, y-23)
	time.sleep(0.2)
	clickLB(x+50, y+212-23)
	time.sleep(1)
	pyautogui.moveTo(264, 560)
	pyautogui.mouseDown()
	pyautogui.moveTo(150, 574, duration=0.2)
	time.sleep(0.2)
	pyautogui.mouseUp()

	clickLB(2415, 210-23)
	time.sleep(10)
	for i in range(20):
		statY = find_station()
		if (statY):
			break
		if (i == 29):
			print('что-то не то')
			exit(0)
		time.sleep(1)

	clickLB(825, 265-23)
	time.sleep(2)
	clickRB(825, 265-23)
	time.sleep(0.2)
	clickLB(825+60, 265+162-23)
	time.sleep(0.2)
	clickLB(825+300, 265+200-23)
	time.sleep(0.2)
	clickLB(825+420, 265+200-23)

	check_state(5)

def find_station():
	x, y, w, h = 0, 0, 0, 0

	im = get_background_window(hWnd)
	image = im.crop( (XgridType1, YgridType1-23, XgridType2, YgridType2-23) )
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
				(fuzz.token_set_ratio(el[11], 'Trading')) > 70
				# or
				# (fuzz.token_set_ratio(el[11], 'Abyssal')) > 70
			):
				x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])
				break
		except IndexError:
			pass
			# print("Операция была пропущена")

	if (y != 0):
		print('station found')
		y = y+int(h/2)
		return y
	print('station not found')
	return False

def find_bnt_undock():
	for i in range(20):
		im = get_background_window(hWnd)
		image_grid_row = im.crop( (XbtnUndock1, YbtnUndock1-23, XbtnUndock2, YbtnUndock2-23) )

		img_array = np.asarray(image_grid_row)

		bgr_for_hsv = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)

		cat_hsv = cv2.cvtColor(bgr_for_hsv, cv2.COLOR_BGR2HSV)
		cat_color_low_yellow = (23,50,50) #более желтый ненасыщенный
		cat_color_high_yellow = (55,255,255) #темно желтый
		only_cat_hsv = cv2.inRange(cat_hsv, cat_color_low_yellow, cat_color_high_yellow)

		# calculate moments of binary image
		M = cv2.moments(only_cat_hsv)
		if (M["m00"] != 0):
			print('ship docked')
			
			return
		else:
			print('ship go to station')
			time.sleep(5)
	print('не видит кнопку')
	exit(0)




















def find_filament():
	im = get_background_window(hWnd)
	image_cargo = im.crop( (222, 530-23, 788, 968-23) )

	img = np.asarray(image_cargo)

	config = r'--oem 3 --psm 6'

	data = pytesseract.image_to_data(img, config=config)

	# Перебираем данные про текстовые надписи
	for i, el in enumerate(data.splitlines()):
		if i == 0:
			continue

		el = el.split()
		try:
			if(
				(fuzz.token_set_ratio(el[11], 'Exotic')) > 50
			):
				print(el[11], fuzz.token_set_ratio(el[11], 'Exotic'))

				x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])

				# image_elem = image_cargo.crop( (x, y-25, x+w, y+h) )

				image_elem = image_cargo.crop( (x-38, y-5, x+w, y+h+5) )

				img1 = np.asarray(image_elem)

				data1 = pytesseract.image_to_data(img1, config=config)

				for i1, el1 in enumerate(data1.splitlines()):
					if i1 == 0:
						continue

					el1 = el1.split()
					try:
						if(
							(fuzz.token_set_ratio(el1[11], 'Calm')) > 50
						):
							print(el1[11], fuzz.token_set_ratio(el1[11], 'Calm'))
							# return 222+x+int(w/2), 632+y-30
							return 222+x, 530+y
					except IndexError:
						pass
		except IndexError:
			pass
	return 0, 0

def find_trace():
	x, y, w, h = 0, 0, 0, 0

	im = get_background_window(hWnd)
	image = im.crop( (XgridType1, YgridType1-23, XgridType2, YgridType2-23) )
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
				(fuzz.token_set_ratio(el[11], 'Conduit')) > 70
				or
				(fuzz.token_set_ratio(el[11], 'Abyssal')) > 70
			):
				x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])
				break
		except IndexError:
			pass
			# print("Операция была пропущена")

	if (y != 0):
		print('trace detected')
		y = y+int(h/2)
		return y
	print('trace NOT detected')
	return False

def find_cont():
	x, y, w, h = 0, 0, 0, 0

	im = get_background_window(hWnd)
	image = im.crop( (XgridType1, YgridType1-23, XgridType2, YgridType2-23) )
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
				(fuzz.token_set_ratio(el[11], 'Biocomb')) > 50
				or
				(fuzz.token_set_ratio(el[11], 'Biocombinative')) > 50
			):
				x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])
				break
		except IndexError:
			pass
			# print("Операция была пропущена")

	if (y != 0):
		print('Biocomb detected')
		y = y+int(h/2)
		return y
	print('Biocomb NOT detected')
	return False


def find_krabidos():
	x, y, w, h = 0, 0, 0, 0

	im = get_background_window(hWnd)
	image = im.crop( (XgridType1, YgridType1-23, XgridType2, YgridType2-23) )
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
				# (fuzz.token_set_ratio(el[11], 'Trace')) > 70
				# or
				(fuzz.token_set_ratio(el[11], 'Foothold')) > 70
			):
				x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])
				break
		except IndexError:
			pass
			# print("Операция была пропущена")

	if (y != 0):
		print('Karibdis detected')
		y = y+int(h/2)
		return y
	print('Karibdis NOT detected')
	return False

def find_skybreaker():
	x, y, w, h = 0, 0, 0, 0

	im = get_background_window(hWnd)
	image = im.crop( (XgridType1, YgridType1-23, XgridType2, YgridType2-23) )
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
				(fuzz.token_set_ratio(el[11], 'Pacifier')) > 70
				or
				(fuzz.token_set_ratio(el[11], 'Skybreaker')) > 70
			):
				x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])
				break
		except IndexError:
			pass
			# print("Операция была пропущена")

	if (y != 0):
		print('Skybreaker detected')
		y = y+int(h/2)
		return y
	print('Skybreaker NOT detected')
	return False

def find_frigate():
	x, y, w, h = 0, 0, 0, 0

	im = get_background_window(hWnd)
	image = im.crop( (XgridType1, YgridType1-23, XgridType2, YgridType2-23) )
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
				(fuzz.token_set_ratio(el[11], 'Lancer')) > 70
				or
				(fuzz.token_set_ratio(el[11], 'Damavik')) > 70
				or
				(fuzz.token_set_ratio(el[11], 'Cynabal')) > 70
				or
				(fuzz.token_set_ratio(el[11], 'Echo')) > 70
				or
				(fuzz.token_set_ratio(el[11], 'Ephialtes')) > 70
				or
				(fuzz.token_set_ratio(el[11], 'Spearfis')) > 70
				or
				(fuzz.token_set_ratio(el[11], 'Nullwarp')) > 70
			):
				x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])
				break
		except IndexError:
			pass
			# print("Операция была пропущена")

	if (y != 0):
		print('frigates detected')
		y = y+int(h/2)
		return y
	print('frigates NOT detected')
	return False

def find_devoted_knight():
	x, y, w, h = 0, 0, 0, 0

	im = get_background_window(hWnd)
	image = im.crop( (XgridType1, YgridType1-23, XgridType2, YgridType2-23) )
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
				(fuzz.token_set_ratio(el[11], 'Devoted')) > 70
				and
				(fuzz.token_set_ratio(el[11], 'Knight')) > 70
			):
				x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])
				break
		except IndexError:
			pass
			# print("Операция была пропущена")

	if (y != 0):
		print('devoted knight detected')
		y = y+int(h/2)
		return y
	print('devoted knight NOT detected')
	return False

def find_devote():
	x, y, w, h = 0, 0, 0, 0

	im = get_background_window(hWnd)
	image = im.crop( (XgridType1, YgridType1-23, XgridType2, YgridType2-23) )
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
				(fuzz.token_set_ratio(el[11], 'devoted')) > 70
			):
				x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])
				break
		except IndexError:
			pass
			# print("Операция была пропущена")

	if (y != 0):
		print('devoted detected')
		y = y+int(h/2)
		return y
	print('devoted NOT detected')
	return False

def find_vila():
	x, y, w, h = 0, 0, 0, 0

	im = get_background_window(hWnd)
	image = im.crop( (XgridType1, YgridType1-23, XgridType2, YgridType2-23) )
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
				(fuzz.token_set_ratio(el[11], 'Swarmer')) > 70
				# or
				# (fuzz.token_set_ratio(el[11], 'Skybreaker')) > 70
			):
				x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])
				break
		except IndexError:
			pass
			# print("Операция была пропущена")

	if (y != 0):
		print('Swarmer detected')
		y = y+int(h/2)
		return y
	print('Swarmer NOT detected')
	return False

def find_remove_btn(x1, y1):
	x, y, w, h = 0, 0, 0, 0

	im = get_background_window(hWnd)
	image = im.crop( (x1, y1-23, x1+60, y1+230-23) )
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
				(fuzz.token_set_ratio(el[11], 'Remove')) > 70
				# or
				# (fuzz.token_set_ratio(el[11], 'Skybreaker')) > 70
			):
				x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])
				break
		except IndexError:
			pass
			# print("Операция была пропущена")

	if (y != 0):
		print('Remove btn found')
		y = y+int(h/2)
		return y
	print('Remove btn NOT found')
	return False

def lock_state(sec):
	time.sleep(sec)
	cnt_lock = 0
	while True:
		im = get_background_window(hWnd)
		image = im.crop( (Xgrid1, Ygrid1-23, Xgrid2, Ygrid2-23) )

		image = np.asarray(image)

		image_bgr = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

		image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV) #Преобразуем в HSV

		image_hsv_low = (0,0,255)# белый
		image_hsv_high = (0,0,255)# белый
		white_mask = cv2.inRange(image_hsv, image_hsv_low, image_hsv_high)

		# calculate moments of binary image
		M = cv2.moments(white_mask)

		if(M["m00"] != 0):
			print('target locked')
			
			return False
		else:
			drones_hp_state()
			print('target still locking')
			time.sleep(1)
			cnt_lock += 1
			if(cnt_lock>2):
				print('bad try')
				return True

def engage_state():
	cnt = 0
	cnt_atack = 0
	cd_scoop = 0
	while True:
		im = get_background_window(hWnd)
		image_grid_row = im.crop( (Xgrid1, Ygrid1-23, Xgrid2, Ygrid2-23) )

		img_array = np.asarray(image_grid_row)

		bgr_for_hsv = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)

		cat_hsv = cv2.cvtColor(bgr_for_hsv, cv2.COLOR_BGR2HSV) #Преобразуем в HSV

		cat_color_low_white = (0,0,255)# белый
		cat_color_high_white = (0,0,255)# белый
		only_cat_hsv = cv2.inRange(cat_hsv, cat_color_low_white, cat_color_high_white)


		# calculate moments of binary image
		M = cv2.moments(only_cat_hsv)


		if(M["m00"] != 0):
			
			if(cnt > 2):
				('unluck background or white arrows')
				break
			if(engage_target() == 0):
				cnt = 0
				cnt_atack += 1
				if (cnt_atack > 8):
					cnt_atack = 0
					press_btn(0x46)
			else:
				cnt += 1

			#cd to scoop drones
			if(cd_scoop == 0):
				if(drones_hp_state()):
					cd_scoop = 12
			if(cd_scoop != 0):
				cd_scoop -= 1
			time.sleep(1)
		else:
			print('target destroyed')
			time.sleep(1)
			break

def engage_target():
	im = get_background_window(hWnd)
	image_drones = im.crop( (XdroneMod1, YdroneMod1-23, XdroneMod2, YdroneMod2-23) )

	img_array_dr = np.asarray(image_drones)

	bgr_for_hsv = cv2.cvtColor(img_array_dr, cv2.COLOR_BGR2RGB)

	cat_hsv = cv2.cvtColor(bgr_for_hsv, cv2.COLOR_BGR2HSV) #Преобразуем в HSV
	cat_color_low_green = (50,52,72) #более зеленый ненасыщенный
	cat_color_high_green = (85,255,255) #темно зеленый
	only_cat_hsv_green = cv2.inRange(cat_hsv, cat_color_low_green, cat_color_high_green)


	cat_color_low_red = (0,155,84) #более красный ненасыщенный
	cat_color_high_red = (15,255,255) #темно красный
	only_cat_hsv_red = cv2.inRange(cat_hsv, cat_color_low_red, cat_color_high_red)

	# calculate moments of binary image
	M_green = cv2.moments(only_cat_hsv_green)
	M_red = cv2.moments(only_cat_hsv_red)

	if(M_red["m00"] != 0):
		return 0
	elif(M_green["m00"] != 0):
		print('drones stay afk')
		press_btn(0x46)
		return 1
	else:
		print('дроны точно есть?')

def drones_hp_state():
	im = get_background_window(hWnd)
	image_drones = im.crop( (XdroneHP1, YdroneHP1-23, XdroneHP2, YdroneHP2-23) )

	img_array_dr = np.asarray(image_drones)

	bgr_for_hsv = cv2.cvtColor(img_array_dr, cv2.COLOR_BGR2RGB)

	cat_hsv = cv2.cvtColor(bgr_for_hsv, cv2.COLOR_BGR2HSV) #Преобразуем в HSV

	cat_color_low_red = (150,209,150) #более красный ненасыщенный
	cat_color_high_red = (255,255,255) #темно красный
	only_cat_hsv_red = cv2.inRange(cat_hsv, cat_color_low_red, cat_color_high_red)

	# calculate moments of binary image
	M_red = cv2.moments(only_cat_hsv_red)

	if(M_red["m00"] != 0):
		print('rescoop drones')
		raise_drone()
		time.sleep(3)
		print('drop drones')
		drop_drone()
		return True
	else:
		return False

def find_targets():
	for i in range(40):
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
			print('ship jumped')
			return
		else:
			print('ship go to next room')
			time.sleep(3)

def add_enemy_to_grid():
	pass

def approach_state():
	tryes = 0
	while True:
		im = get_background_window(hWnd)
		img_state = im.crop( (XmiddleText1, YmiddleText1-23, XmiddleText2, YmiddleText2-23) )

		img_state_string = np.asarray(img_state)

		rgb_state = cv2.cvtColor(img_state_string, cv2.COLOR_BGR2RGB)


		psm4_state = pytesseract.image_to_string(rgb_state, config='--psm 4')
		psm6_state = pytesseract.image_to_string(rgb_state, config='--psm 6')
		if(
			(fuzz.token_set_ratio(psm4_state, 'APPROACHING')) > 50
			or
			(fuzz.token_set_ratio(psm6_state, 'APPROACHING')) > 50
		):
			if(tryes > 12):
				print('произошел вылет из игры')
				exit(0)
			tryes += 1
			print('ship still approach...')
			time.sleep(5)
		else:
			time.sleep(10)
			print('ship jumped')
			break

def check_state(sec):
	time.sleep(3.5)
	tryes = 0
	if(sec == 5):
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
				if(tryes > 20):
					print('произошел вылет из игры')
					exit(0)
				tryes += 1
				print('ship still warping...')
				time.sleep(sec)
			else:
				print('ship finished warping')
				break


def drop_drone():
	press_btn(0x47)

	time.sleep(1.5)
	i = 0
	for i in range(8):
		im = get_background_window(hWnd)
		image_drones = im.crop( (XdroneMod1, YdroneMod1-23, XdroneMod2, YdroneMod2-23) )

		img_array_dr = np.asarray(image_drones)

		bgr_for_hsv = cv2.cvtColor(img_array_dr, cv2.COLOR_BGR2RGB)

		cat_hsv = cv2.cvtColor(bgr_for_hsv, cv2.COLOR_BGR2HSV) #Преобразуем в HSV
		cat_color_low_green = (50,52,72) #более зеленый ненасыщенный
		cat_color_high_green = (85,255,255) #темно зеленый
		only_cat_hsv_green = cv2.inRange(cat_hsv, cat_color_low_green, cat_color_high_green)


		cat_color_low_red = (0,155,84) #более красный ненасыщенный
		cat_color_high_red = (15,255,255) #темно красный
		only_cat_hsv_red = cv2.inRange(cat_hsv, cat_color_low_red, cat_color_high_red)

		# calculate moments of binary image
		M_green = cv2.moments(only_cat_hsv_green)
		M_red = cv2.moments(only_cat_hsv_red)

		if((M_red["m00"] != 0) or (M_green["m00"] != 0)):
			return
		elif((M_red["m00"] == 0) and (M_green["m00"] == 0)):
			print('drones not launch')
			press_btn(0x47)
			time.sleep(1.5)
	print('дроны не запускаются')

def raise_drone():
	press_btn(0x48)
	i = 0
	for i in range(3):
		im = get_background_window(hWnd)
		image_grid_row = im.crop( (XdroneMod1, YdroneMod1-23, XdroneMod2, YdroneMod2-23) )

		img_array = np.asarray(image_grid_row)

		bgr_for_hsv = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)

		cat_hsv = cv2.cvtColor(bgr_for_hsv, cv2.COLOR_BGR2HSV) #Преобразуем в HSV
		cat_color_low_yellow = (25,180,150) #более желтый ненасыщенный
		cat_color_high_yellow = (35,255,255) #темно желтый
		only_cat_hsv_yellow = cv2.inRange(cat_hsv, cat_color_low_yellow, cat_color_high_yellow)

		cat_color_low_green = (50,52,72) #более зеленый ненасыщенный
		cat_color_high_green = (85,255,255) #темно зеленый
		only_cat_hsv_green = cv2.inRange(cat_hsv, cat_color_low_green, cat_color_high_green)

		cat_color_low_red = (0,155,84) #более красный ненасыщенный
		cat_color_high_red = (15,255,255) #темно красный
		only_cat_hsv_red = cv2.inRange(cat_hsv, cat_color_low_red, cat_color_high_red)

		# calculate moments of binary image
		M_yellow = cv2.moments(only_cat_hsv_yellow)
		M_green = cv2.moments(only_cat_hsv_green)
		M_red = cv2.moments(only_cat_hsv_red)

		if((M_green["m00"] != 0) or (M_red["m00"] != 0)):
			if (i>=2):
				print('bad try, unluck bg, close game or bad coords')
			print('drones not comeback, attempt to raise...')
			press_btn(0x48)
			time.sleep(3)
		if(M_yellow["m00"] != 0):
			print('drones comeback')
			break

	for i in range(30):
		im = get_background_window(hWnd)
		image_grid_row = im.crop( (XdroneMod1, YdroneMod1-23, XdroneMod2, YdroneMod2-23) )

		img_array = np.asarray(image_grid_row)

		bgr_for_hsv = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)

		cat_hsv = cv2.cvtColor(bgr_for_hsv, cv2.COLOR_BGR2HSV) #Преобразуем в HSV
		cat_color_low_yellow = (25,180,150) #более желтый ненасыщенный
		cat_color_high_yellow = (35,255,255) #темно желтый
		only_cat_hsv_yellow = cv2.inRange(cat_hsv, cat_color_low_yellow, cat_color_high_yellow)

		# calculate moments of binary image
		M_yellow = cv2.moments(only_cat_hsv_yellow)

		if(M_yellow["m00"] != 0):
			print('drones are still going...')
			time.sleep(2)
		else:
			print('drones are raised')
			break

def destroy_targets():
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


	if (M["m00"] == 0):
		print('all targets destroyed')
		return
	while True:
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
			cX = int(M["m10"] / M["m00"])
			cY = int(M["m01"] / M["m00"])

			print('lock next target')
			lock_target(cY)
			
			lock_state(2)
			
			engage_state()
		else:
			print('all targets destroyed')
			return

def activate_filament():
	for i in range(3):
		clickRB(XwndSpace, YwndSpace)
		time.sleep(0.2)
		clickLB(XwndSpace+50, YwndSpace+70) # sort
		time.sleep(2)
		x, y = find_filament()
		if (y != 0):
			break
		if (i == 2):
			print('no calm exotic')
			exit(0)
		print('bad try to find filament')
	for i in range(3):
		clickRB(x, y-23)
		time.sleep(0.2)
		clickLB(x+50, y+165-23)
		time.sleep(1)
		clickLB(XactivateFilament, YactivateFilament-23)###
		time.sleep(3.5)
		y1 = find_trace()
		if(y1):
			clickLB(Xgrid2, Ygrid1+y1-23)
			time.sleep(1)
			clickLB(gateCoordsX, gateCoordsY-23)
			time.sleep(1)
			clickLB(XEnterToDange, YEnterToDange-23)###
			return
	print('not enough calm exotic')
	exit(0)
		

def Goto():
	for i in range(3):
		y = find_trace()
		if(y):
			clickLB(Xgrid2, Ygrid1+y-23)
			time.sleep(0.2)
			clickLB(gateCoordsX, gateCoordsY-23)
			return

def open_cont():
	for i in range(60):
		im = get_background_window(hWnd)
		image = im.crop( (XopenedCont1, YopenedCont1-23, XopenedCont2, YopenedCont2-23) )
		image = np.asarray(image)

		config = r'--oem 3 --psm 6'

		data = pytesseract.image_to_data(image, config=config)

		for i, el in enumerate(data.splitlines()):
			if i == 0:
				continue

			el = el.split()
			try:
				if(
					(fuzz.token_set_ratio(el[11], 'Triglavian')) > 70
					# or
					# (fuzz.token_set_ratio(el[11], 'Biocombinative')) > 70
				):
					# x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])
					print('Triglavian cont opened')
					clickLB(XtakeAllBtnCoords, YtakeAllBtnCoords-23) # take all
					return True
			except IndexError:
				pass
				# print("Операция была пропущена")
		time.sleep(0.2)
		clickLB(gateCoordsX, gateCoordsY-23) # loot
		time.sleep(0.5)
	print('собственно конт не нашелся')
	return False

def loot_cont():
	for i in range(5):
		im = get_background_window(hWnd)
		image = im.crop( (XopenedCont1, YopenedCont1-23, XopenedCont2, YopenedCont2-23) )
		image = np.asarray(image)

		config = r'--oem 3 --psm 6'

		data = pytesseract.image_to_data(image, config=config)

		for i, el in enumerate(data.splitlines()):
			if i == 0:
				continue

			el = el.split()
			try:
				print(fuzz.token_set_ratio(el[11], 'Triglavian'))
				if(
					(fuzz.token_set_ratio(el[11], 'Triglavian')) < 70
					# or
					# (fuzz.token_set_ratio(el[11], 'Biocombinative')) > 70
				):
					# x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])
					print('Triglavian cont looted')
					return
			except IndexError:
				print('except')
				pass
				# print("Операция была пропущена")
		clickLB(XtakeAllBtnCoords, YtakeAllBtnCoords-23) # loot
		time.sleep(4)
	print('cont NOT looted')


while True:
	# check_drones_quantity()

	# # if (check_cargo()):
	# # 	unload_cargo()
		
	# # check_DT()

	# date = datetime.datetime.today()
	# print('start farm dungeon: ' + date.strftime('%H:%M'))

	# clickLB(X1vkladka, Y1vkladka-23)
	# time.sleep(1)
	# activate_filament()
	# time.sleep(15)
	# find_targets()
	# clickLB(Xgrid2, Ygrid1+10-23)
	# time.sleep(0.2)
	# clickLB(gateCoordsX+30, gateCoordsY-23)
	# time.sleep(0.5)
	# press_btn(0x70) # ab on
	# # press_btn(0x71)

	for i in range(3):
		im = get_background_window(hWnd)
		im.save('LAST_SCREENSHOT.jpg')

		drop_drone()

		
		krabY = find_krabidos()
		if (krabY):
			clickLB(Xgrid2, Ygrid1+krabY-23)
			time.sleep(0.2)
			clickLB(gateCoordsX, gateCoordsY-23) # orbit
			while True:
				lock_target(krabY)
				if (lock_state(2)):
					lock_target(krabY) ###
				else:
					break
			press_btn(0x46)

			engage_state()

		skybY = find_skybreaker()
		if (skybY):
			y = find_trace()
			if(y):
				clickLB(Xgrid2, Ygrid1+y-23)
				time.sleep(1)
				clickLB(gateCoordsX+30, gateCoordsY-23)
			press_btn(0x70) # ab on
			destroy_targets()
			press_btn(0x70) # ab on

		vilaY = find_vila()
		if (vilaY):
			while (True):
				clickRB(Xgrid2, Ygrid1+vilaY-23)
				time.sleep(0.3)
				removeY = find_remove_btn(Xgrid2+10, Ygrid1+vilaY)
				if (removeY):
					clickLB(Xgrid2+60, Ygrid1+vilaY+removeY-23)
					break
				time.sleep(0.5)
				# vilaY = find_vila()
			press_btn(0x70) # ab on
			destroy_targets()
			press_btn(0x70) # ab on

		tesY = find_frigate()
		if (tesY):
			y = find_trace()
			if(y):
				clickLB(Xgrid2, Ygrid1+y-23)
				time.sleep(0.2)
				clickLB(gateCoordsX+30, gateCoordsY-23)
			press_btn(0x70) # ab on
			destroy_targets()
			press_btn(0x70) # ab on

		devoY = find_devoted_knight()
		if (devoY):
			y = find_trace()
			if(y):
				clickRB(Xgrid2, Ygrid1+y-23)
				time.sleep(0.2)
				clickLB(Xgrid2+50, Ygrid1+y+35-23)
				time.sleep(0.2)
				clickLB(Xgrid2+300, Ygrid1+y+206-23) # orbit 30 km
			destroy_targets()

		devoY = find_devote()
		if (devoY):
			y = find_trace()
			if(y):
				clickRB(Xgrid2, Ygrid1+y-23)
				time.sleep(0.2)
				clickLB(Xgrid2+50, Ygrid1+y+35-23)
				time.sleep(0.2)
				clickLB(Xgrid2+300, Ygrid1+y+186-23) # orbit 25 km
			destroy_targets()

		clickLB(X3vkladka, Y3vkladka-23)
		time.sleep(0.5)

		contY = find_cont()
		if(contY):
			clickLB(Xgrid2, Ygrid1+contY-23)
			time.sleep(0.2)
			clickLB(gateCoordsX, gateCoordsY-23) # orbit
		else:
			y = find_trace()
			if(y):
				clickLB(Xgrid2, Ygrid1+y-23)
				time.sleep(0.2)
				clickLB(gateCoordsX+30, gateCoordsY-23)

		clickLB(X1vkladka, Y1vkladka-23)
		time.sleep(0.5)
		# check_prop()
		destroy_targets()

		clickLB(X3vkladka, Y3vkladka-23)
		time.sleep(0.5)
		contY = find_cont()
		if (contY):
			if (contY > 25):
				clickLB(Xgrid2, Ygrid1+contY-23)
				time.sleep(0.2)
				clickLB(gateCoordsX-66, gateCoordsY-23) # approach
				while True:
					lock_target(contY)
					if (lock_state(1)):
						lock_target(contY) ###
					else:
						break

				time.sleep(1)
				clickLB(gateCoordsX-66, gateCoordsY-23) # approach

				press_btn(0x46)

				engage_state()

				press_btn(0x48)

				time.sleep(0.2)

				clickLB(XconstVel, YconstVel-23) # 1400
				# time.sleep(0.2)

				contY = find_cont()
				if(contY):
					clickLB(Xgrid2, Ygrid1+contY-23)
					time.sleep(0.1)
					clickLB(gateCoordsX, gateCoordsY-23) # loot
					opened = open_cont()  # приемлемая скорость 1200-1400
					if (opened):
						time.sleep(0.5)
						loot_cont()
				else:
					print('конт не нашелся')
			else:
				press_btn(0x48)
				clickLB(XconstVel, YconstVel-23) # 1400
				time.sleep(0.2)
				clickLB(Xgrid2, Ygrid1+contY-23)
				time.sleep(0.2)
				clickLB(gateCoordsX, gateCoordsY-23) # loot
				opened = open_cont()  # приемлемая скорость 1200-1400
				if (opened):
					time.sleep(0.5)
					loot_cont()

		raise_drone()

		clickLB(XmaxVel, YmaxVel-23) # max vel
		time.sleep(0.2)

		clickLB(X1vkladka, Y1vkladka-23) ### Общие настройки
		time.sleep(0.5)
		Goto()
		time.sleep(10)

		if (i < 2):
			find_targets()
			# if find_targets():
			# 	add_enemy_to_grid()
		# approach_state()
	time.sleep(32)
	clickLB(Xgrid2, Ygrid1+10-23)
	for i in range(20):
		y = find_trace()
		if(y):
			time.sleep(5)
		else:
			break
	clickLB(gateCoordsX-66, gateCoordsY-23)
	time.sleep(1)
	clickLB(X0Vel, Y0Vel-23) # ship stop