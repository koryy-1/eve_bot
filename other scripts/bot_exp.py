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

moveToX = 2240
moveToY = 250

gateCoordsX = 2204
gateCoordsY = 122
prosto_cnt = 0

hWnd = win32gui.FindWindow("trinityWindow", None)

# x, y = pyautogui.position()
# print(x, y)

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

def press_btn(BTN):
	while (win32api.GetKeyState(win32con.VK_CONTROL) < 0 or
			win32api.GetKeyState(win32con.VK_SHIFT) < 0 or
			win32api.GetKeyState(win32con.VK_MENU) < 0
		):
		time.sleep(0.005)
	temp = win32gui.PostMessage(hWnd, win32con.WM_IME_KEYDOWN, BTN, 0)
	time.sleep(0.05)
	temp = win32gui.PostMessage(hWnd, win32con.WM_IME_KEYUP, BTN, 0)
	time.sleep(0.1)

# image.show()


def find_ancient_gate():
	x, y, w, h = 0, 0, 0, 0

	im = get_background_window(hWnd)
	image = im.crop( (2336, 240-23, 2448, 430-23) )
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
				(fuzz.token_set_ratio(el[11], 'Ancient')) > 70
				or
				(fuzz.token_set_ratio(el[11], 'Acceleration')) > 70
			):
				# Создаем подписи на картинке
				x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])
				break
		except IndexError:
			pass
			# print("Операция была пропущена")

	if (y != 0):
		print('acceleration gate detected')
		y = y+int(h/2)
		return y
	print('acceleration gate not detected')
	return False

def find_supply():
	x, y, w, h = 0, 0, 0, 0

	im = get_background_window(hWnd)
	image = im.crop( (2336, 240-23, 2448, 430-23) )
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
				(fuzz.token_set_ratio(el[11], 'Supply')) > 70
				or
				(fuzz.token_set_ratio(el[11], 'Radiating')) > 70
			):
				# Создаем подписи на картинке
				x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])
				break
		except IndexError:
			pass
			# print("Операция была пропущена")

	if (y != 0):
		print('supply detected')
		y = y+int(h/2)
		return y
	print('supply not detected')
	return False


### прыг в следующую систему
def go_next():
	global moveToX
	global moveToY

	global gateCoordsX
	global gateCoordsY
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
		print('корабль прибыл в сисю с экспой')
		return False
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

	clickLB(2240, 227)
	time.sleep(0.2)
	clickLB(2204, 99)
	return True


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
				time.sleep(7)
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
					time.sleep(7)
			break



### захват цели
def check_lock():
	time.sleep(5)
	cnt_lock = 0
	while True:
		im = get_background_window(hWnd)
		image_grid_row = im.crop( (2122, 240-23, 2150, 800-23) )

		img_array = np.asarray(image_grid_row)

		bgr_for_hsv = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)

		cat_hsv = cv2.cvtColor(bgr_for_hsv, cv2.COLOR_BGR2HSV) #Преобразуем в HSV

		cat_color_low_white = (0,0,255)# белый
		cat_color_high_white = (0,0,255)# белый
		only_cat_hsv = cv2.inRange(cat_hsv, cat_color_low_white, cat_color_high_white)

		M = cv2.moments(only_cat_hsv)

		# print('M["m00"] = ' + str(M["m00"]))

		if(M["m00"] != 0):
			print('target locked')
			
			return
		else:
			print('target still locking')
			time.sleep(1)
			cnt_lock += 1
			if(cnt_lock>3):
				print('bad try')
				return

def engage_target():
	im = get_background_window(hWnd)
	image_drones = im.crop( (1884, 930-23, 2032, 1040-23) )

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
		print('drones stay afk, engage target')
		# pyautogui.press('f')
		# time.sleep(0.25)
		# pyautogui.keyDown('f')
		# time.sleep(0.25)
		# pyautogui.keyUp('f')
		# time.sleep(0.25)
		# pyautogui.keyDown('f')
		# time.sleep(0.25)
		# pyautogui.keyUp('f')
		# time.sleep(0.25)

		while (win32api.GetKeyState(win32con.VK_CONTROL) < 0 or
				win32api.GetKeyState(win32con.VK_SHIFT) < 0 or
				win32api.GetKeyState(win32con.VK_MENU) < 0
			):
			time.sleep(0.005)
		temp = win32gui.PostMessage(hWnd, win32con.WM_IME_KEYDOWN, 0x46, 0)
		time.sleep(0.05)
		temp = win32gui.PostMessage(hWnd, win32con.WM_IME_KEYUP, 0x46, 0)
		time.sleep(0.1)
		return 1
	else:
		print('кнопки не нажимаются, поменяй раскладку')
		exit(0)


### чтение грида на наличие NPC
def check_grid():
	# im = get_background_window(hWnd)
	# image_drones = im.crop( (1884, 930-23, 2032, 1040-23) )
	# img_grid = ImageGrab.grab( (2122, 225, 2150, 800) ) # grid

	# img_grid_string = np.asarray(img_grid)

	# rgb_grid = cv2.cvtColor(img_grid_string, cv2.COLOR_BGR2RGB)

	try:
		while True:
			cnt_farm = 0
			im = get_background_window(hWnd)
			image_grid_row = im.crop( (2122, 240-23, 2150, 800-23) )

			img_array = np.asarray(image_grid_row)

			bgr_for_hsv = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)

			cat_hsv = cv2.cvtColor(bgr_for_hsv, cv2.COLOR_BGR2HSV) #Преобразуем в HSV
			cat_color_low_red = (0,155,84) #более красный ненасыщенный
			cat_color_high_red = (15,255,255) #темно красный
			only_cat_hsv = cv2.inRange(cat_hsv, cat_color_low_red, cat_color_high_red)


			# calculate moments of binary image
			M = cv2.moments(only_cat_hsv)

			# calculate x,y coordinate of center
			cX = int(M["m10"] / M["m00"])
			cY = int(M["m01"] / M["m00"])

			# pyautogui.moveTo(2117 + cX, 240 + cY,)
			# pyautogui.keyDown('ctrl')
			# time.sleep(0.2)
			# pyautogui.click()
			# pyautogui.keyUp('ctrl')
			# pyautogui.moveTo(2050 + cX, 240 + cY, duration=0.1)

			lParam1 = win32api.MAKELONG(2117 + cX, 217 + cY)
			lParam2 = win32api.MAKELONG(2050 + cX, 217 + cY)
			while (win32api.GetKeyState(win32con.VK_CONTROL) < 0 or
					win32api.GetKeyState(win32con.VK_SHIFT) < 0 or
					win32api.GetKeyState(win32con.VK_MENU) < 0
				):
				time.sleep(0.005)
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

			
			check_lock()

			
			while True:
				im = get_background_window(hWnd)
				image_grid_row = im.crop( (2122, 240-23, 2150, 800-23) )

				img_array = np.asarray(image_grid_row)

				bgr_for_hsv = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)

				cat_hsv = cv2.cvtColor(bgr_for_hsv, cv2.COLOR_BGR2HSV) #Преобразуем в HSV

				cat_color_low_white = (0,0,255)# белый
				cat_color_high_white = (0,0,255)# белый
				only_cat_hsv = cv2.inRange(cat_hsv, cat_color_low_white, cat_color_high_white)


				# calculate moments of binary image
				M = cv2.moments(only_cat_hsv)


				# calculate x,y coordinate of center
				# cX = int(M["m10"] / M["m00"])
				# cY = int(M["m01"] / M["m00"])

				# M["m00"].is_integer()

				if(M["m00"] != 0):
					
					if(cnt_farm > 2):
						('unluck background or white arrows')
						break
					if(engage_target() == 0):
						cnt_farm = 0
					else:
						cnt_farm += 1
					time.sleep(2)
				else:
					print('lock next target')
					time.sleep(1.5)
					break
	except Exception as e:
		print(e)

def drop_drone():
	# pyautogui.keyDown('shift')
	# time.sleep(0.2)
	# pyautogui.press('f')
	# # time.sleep(0.25)
	# # pyautogui.press('f')
	# # time.sleep(0.25)
	# # pyautogui.keyDown('f')
	# # time.sleep(0.25)
	# # pyautogui.keyUp('f')
	# # time.sleep(0.25)
	# # pyautogui.keyDown('f')
	# # time.sleep(0.25)
	# # pyautogui.keyUp('f')
	# # time.sleep(0.25)
	# # pyautogui.press('f')
	# # time.sleep(0.25)
	# pyautogui.keyUp('shift')

	# clickRB(1932, 854)
	# time.sleep(0.4)
	# clickLB(1972, 866)
	# time.sleep(0.5)
	# clickLB(2520, 677)

	press_btn(0x47)

	time.sleep(3)
	i = 0
	for i in range(6):
		im = get_background_window(hWnd)
		image_drones = im.crop( (1884, 930-23, 2032, 1040-23) )

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
			# clickRB(1932, 854)
			# time.sleep(0.4)
			# clickLB(1972, 866)

			press_btn(0x47)
			time.sleep(1)
	print('дроны не запускаются')
	exit(0)

def raise_drone():
	# pyautogui.keyDown('shift')
	# time.sleep(0.25)
	# pyautogui.press('r')
	# # time.sleep(0.25)
	# # pyautogui.press('r')
	# # time.sleep(0.25)
	# # pyautogui.keyDown('r')
	# # time.sleep(0.25)
	# # pyautogui.keyUp('r')
	# # time.sleep(0.25)
	# # pyautogui.keyDown('r')
	# # time.sleep(0.25)
	# # pyautogui.keyUp('r')
	# # time.sleep(0.25)
	# # pyautogui.press('r')
	# # time.sleep(0.25)
	# pyautogui.keyUp('shift')
	# pyautogui.hotkey('shift', 'r')

	# clickRB(1932, 898)
	# time.sleep(0.2)
	# clickLB(1972, 960)

	press_btn(0x48)

	time.sleep(5)
	i = 0
	for i in range(3):
		im = get_background_window(hWnd)
		image_grid_row = im.crop( (1884, 930-23, 2032, 1040-23) )

		img_array = np.asarray(image_grid_row)

		bgr_for_hsv = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)

		cat_hsv = cv2.cvtColor(bgr_for_hsv, cv2.COLOR_BGR2HSV) #Преобразуем в HSV
		cat_color_low_yellow = (25,180,150) #более желтый ненасыщенный
		cat_color_high_yellow = (35,255,255) #темно желтый
		only_cat_hsv_yellow = cv2.inRange(cat_hsv, cat_color_low_yellow, cat_color_high_yellow)

		cat_color_low_green = (50,52,72) #более зеленый ненасыщенный
		cat_color_high_green = (85,255,255) #темно зеленый
		only_cat_hsv_green = cv2.inRange(cat_hsv, cat_color_low_green, cat_color_high_green)

		# calculate moments of binary image
		M_yellow = cv2.moments(only_cat_hsv_yellow)
		M_green = cv2.moments(only_cat_hsv_green)

		if((M_green["m00"] != 0) and (M_yellow["m00"] == 0)):
			if (i>=2):
				print('bad try, unluck bg, close game or bad coords')
				exit(0)
			print('drones stay afk, attempt to raise...')
			# pyautogui.keyDown('shift')
			# time.sleep(0.25)
			# pyautogui.press('r')
			# pyautogui.keyUp('shift')

			# clickRB(1932, 898)
			# time.sleep(0.2)
			# clickLB(1972, 960)
			# time.sleep(0.5)
			# clickLB(2520, 677)

			press_btn(0x48)
			time.sleep(3)
		if(M_yellow["m00"] != 0):
			print('drones comeback')
			break

	while True:
		im = get_background_window(hWnd)
		image_grid_row = im.crop( (1884, 930-23, 2032, 1040-23) )

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
			clickLB(2520, 677)
			break

### запуск функции фарма
def farm_NPC():
	print('start to farm exp')
	
	# check_gate()

	# check_state(5)

	print('droping drones')

	drop_drone()

	check_grid()

	print('raising drones...')

	raise_drone()

	print('sector clear')




while go_next():
	check_state(10)

clickLB(20, 135-23)
time.sleep(1)
clickLB(1670, 933-23)
time.sleep(1)
clickLB(20, 135-23)

check_state(5)
print('корабль прилетел в экспу')

press_btn(0x71)
# pyautogui.press('f2')
# time.sleep(0.25)
# pyautogui.press('f3')

date = datetime.datetime.today()
print('bot start farm exp at: ' + date.strftime('%H:%M'))

while True:
	row = find_ancient_gate()
	if (row):
		clickLB(2350, 240+row-23)
		time.sleep(0.2)
		clickLB(gateCoordsX, gateCoordsY-23)
		check_state(5)

	row = find_ancient_gate()
	if (row):
		clickLB(2350, 240+row-23)
		time.sleep(0.2)
		clickLB(gateCoordsX-66, gateCoordsY-23) # approach
		press_btn(0x70)
		# pyautogui.press('f1')
	else:
		break
	farm_NPC()
clickLB(2133, 232-23)
time.sleep(1)
print('check supply or telescope')
contY = find_supply()
if(contY):
	clickLB(2245, 240+contY-23)
	time.sleep(0.2)
	clickLB(gateCoordsX, gateCoordsY-23)
	press_btn(0x70)

farm_NPC()

contY = find_supply()
if(contY):
	clickLB(2245, 240+contY-23)
	time.sleep(0.2)
	clickLB(gateCoordsX-66, gateCoordsY-23) # approach
	press_btn(0x70)

print('destroy supply or telescope')
contY = find_supply()
if(contY):
	lParam1 = win32api.MAKELONG(2245, 240+contY-23)
	lParam2 = win32api.MAKELONG(2050, 240+contY-23)
	while (win32api.GetKeyState(win32con.VK_CONTROL) < 0 or
			win32api.GetKeyState(win32con.VK_SHIFT) < 0 or
			win32api.GetKeyState(win32con.VK_MENU) < 0
		):
		time.sleep(0.005)
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

	
	press_btn(0x47)

	check_lock()

	time.sleep(1)
	press_btn(0x46)
	# pyautogui.press('f')
	print('attack supply')
	time.sleep(0.2)
	clickLB(2133, 232-23)
	date = datetime.datetime.today()
	print('bot end at: ' + date.strftime('%H:%M'))
	exit(0)
