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
from config import *
from ctypes import windll

from fuzzywuzzy import fuzz

# проверка hwnd клиента + проверка на вылеты

hWnd = win32gui.FindWindow(None, 'EVE - AnSiri Senpai')

# print('следующая система:')
current_system4 = ''
current_system6 = ''

# image.show()

is_farming = False
cnt_farmed = 0

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

def clickRB(x1,y1):
	lParam = win32api.MAKELONG(x1, y1)
	while (win32api.GetKeyState(win32con.VK_CONTROL) < 0 or
		   win32api.GetKeyState(win32con.VK_SHIFT) < 0 or
		   win32api.GetKeyState(win32con.VK_MENU) < 0):
		time.sleep(0.005)
	time.sleep(0.1)
	win32gui.PostMessage(hWnd, win32con.WM_MOUSEMOVE, None, lParam)
	time.sleep(0.1)
	win32gui.PostMessage(hWnd, win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON, lParam)
	time.sleep(0.1)
	win32gui.PostMessage(hWnd, win32con.WM_RBUTTONUP, win32con.MK_RBUTTON, lParam)


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


def get_screenshot(x1, y1, x2, y2, hWnd, need2hsv=True):
	im = get_background_window(hWnd)
	image = im.crop( (x1, y1, x2, y2) )
	image = np.asarray(image)
	if need2hsv:
		image_bgr = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV) #Преобразуем в HSV
	return image

def get_mask(h1, s, v, h2, img_hsv):
	low_range = (h1,s,v) #более ненасыщенный цвет
	high_range = (h2,255,255) #темный оттенок
	mask = cv2.inRange(img_hsv, low_range, high_range)
	return mask

def get_mask_moments(img_hsv, color):
	if color == 'green':
		mask = get_mask(50,52,72, 85, img_hsv)
	elif color == 'yellow':
		mask = get_mask(25,180,150, 35, img_hsv)
	elif color == 'red':
		mask = get_mask(0,155,84, 20, img_hsv)
	elif color == 'dark red':
		mask = get_mask(150,209,150, 255, img_hsv)
	elif color == 'orange':
		mask = get_mask(0,155,84, 20, img_hsv)
	elif color == 'white':
		mask = get_mask(0,0,255, 0, img_hsv)
	return cv2.moments(mask)


def lay_route():
	x = 1845
	y = 660
	
	for i in range(8):
		x = 1845
		for j in range(3):
			clickRB(x, y-23)
			time.sleep(0.5)
			clickLB(x+60, y+60-23)
			time.sleep(0.5)
			x += 85
		y += 16
	print('route laid')

### прыг в следующую систему
def go_next():
	global prosto_cnt
	image = get_screenshot(Xgrid1, Ygrid1-23, Xgrid2, Ygrid2-23, hWnd)
	
	M_yellow = get_mask_moments(image, 'yellow')

	if(M_yellow["m00"] == 0):
		if(prosto_cnt < 1):
			prosto_cnt += 1
			time.sleep(8)
			return
		print('route has been completed, a new route is laying')
		lay_route()
	else:
		prosto_cnt = 0

		# x, y = pyautogui.position()

		# if((x == 2204) and (y == 122)):
		# 	pyautogui.click()
		# else:
			# pyautogui.moveTo(moveToX, moveToY)
			# pyautogui.click()
			# time.sleep(0.25)

			# pyautogui.moveTo(gateCoordsX, gateCoordsY)
			# pyautogui.click()

		clickLB(moveToX, moveToY-23)
		time.sleep(0.2)
		clickLB(gateCoordsX, gateCoordsY-23)



### прыг в следующую систему
def go_next_exp():
	image = get_screenshot(Xgrid1, Ygrid1-23, Xgrid2, Ygrid2-23, hWnd)
	
	M_yellow = get_mask_moments(image, 'yellow')

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

	clickLB(moveToX, moveToY-23)
	time.sleep(0.2)
	clickLB(gateCoordsX, gateCoordsY-23)
	return True


### проверка находится ли корабль в варпе
def check_state(sec):
	time.sleep(2.5)
	prosto_cnt = 0
	tryes = 0
	### через проверку надписи WARP
	for i in range(180/sec):
		image = get_screenshot(XmiddleText1, YmiddleText1-23, XmiddleText2, YmiddleText2-23, hWnd)

		psm4_state = pytesseract.image_to_string(image, config='--psm 4')
		psm6_state = pytesseract.image_to_string(image, config='--psm 6')
		if(
			(fuzz.token_set_ratio(psm4_state, 'WARP')) > 50
			or
			(fuzz.token_set_ratio(psm6_state, 'WARP')) > 50
		):
			# if(tryes > 12):
			# 	print('произошел вылет из игры')
			# 	exit(0)
			# tryes += 1
			print('ship still warping...')
			time.sleep(sec)
		else:
			if((sec == 10) and (prosto_cnt < 1)):
				prosto_cnt += 1
				time.sleep(7)
				continue
			print('ship finished warping')
			# current_system4 = next_system4
			# current_system6 = next_system6
			break

# проверка цели на лок
def engage_state():
	cnt = 0
	cnt_atack = 0
	while True:
		image = get_screenshot(Xgrid1, Ygrid1-23, Xgrid2, Ygrid2-23, hWnd)
	
		M_white = get_mask_moments(image, 'white')


		if(M_white["m00"] != 0):
			
			if(cnt > 2):
				('unluck background or white arrows')
				break
			if(engage_target() == 0):
				cnt = 0
				# cnt_atack += 1
				# if (cnt_atack > 20):
				# 	cnt_atack = 0
				# 	press_btn(0x46)
			else:
				cnt += 1

			time.sleep(1)
		else:
			print('target destroyed')
			time.sleep(1)
			break


### проверка находится ли корабль в варпе
def check_state_exp(sec):
	time.sleep(4)
	tryes = 0
	while True:
		image = get_screenshot(XmiddleText1, YmiddleText1-23, XmiddleText2, YmiddleText2-23, hWnd)

		psm4_state = pytesseract.image_to_string(image, config='--psm 4')
		psm6_state = pytesseract.image_to_string(image, config='--psm 6')
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
				image = get_screenshot(XmiddleText1, YmiddleText1-23, XmiddleText2, YmiddleText2-23, hWnd)

				psm4_state = pytesseract.image_to_string(image, config='--psm 4')
				psm6_state = pytesseract.image_to_string(image, config='--psm 6')
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


### процесс захвата цели
def check_lock():
	time.sleep(5)
	cnt_lock = 0
	while True:
		image = get_screenshot(Xgrid1, Ygrid1-23, Xgrid2, Ygrid2-23, hWnd)
	
		M_white = get_mask_moments(image, 'white')


		if(M_white["m00"] != 0):
			print('target locked')
			return
		else:
			print('target still locking')
			time.sleep(1)
			cnt_lock += 1
			if(cnt_lock>3):
				print('bad try')
				return

# хп дронов
def drones_hp_state():
	image = get_screenshot(XdroneHP1, YdroneHP1-23, XdroneHP2, YdroneHP2-23, hWnd)

	M_red = get_mask_moments(image, 'dark red')
	

	if(M_red["m00"] != 0):
		print('rescoop drones')
		raise_drone()
		time.sleep(3)
		print('drop drones')
		drop_drone()
		return True
	else:
		return False

# агра дронов
def engage_target():
	image = get_screenshot(XdroneMod1, YdroneMod1-23, XdroneMod2, YdroneMod2-23, hWnd)

	M_green = get_mask_moments(image, 'green')
	M_red = get_mask_moments(image, 'red')


	if(M_red["m00"] != 0):
		return 0
	elif(M_green["m00"] != 0):
		print('drones stay afk')
		# pyautogui.press('f')
		# time.sleep(0.25)
		# pyautogui.keyDown('f')
		# time.sleep(0.25)
		# pyautogui.keyUp('f')

		press_btn(0x46) # f

		return 1
	else:
		print('дроны точно есть?')
		exit(0)


### чтение грида на наличие NPC
def check_grid():
	image = get_screenshot(Xgrid1, Ygrid1-23, Xgrid2, Ygrid2-23, hWnd)

	M_red = get_mask_moments(image, 'red')

	if (M_red["m00"] == 0):
		print('аномалька уже зафармлена')
		return 0

	print('droping drones')
	drop_drone()
	while True:
		cnt_farm = 0
		cd_scoop = 0

		image = get_screenshot(Xgrid1, Ygrid1-23, Xgrid2, Ygrid2-23, hWnd)

		M_red = get_mask_moments(image, 'red')

		# calculate x,y coordinate of center
		# cX = int(M_red["m10"] / M_red["m00"])
		if M_red["m00"] == 0:
			print('raising drones...')
			raise_drone()

			print('sector clear')
			return 1
		cY = int(M_red["m01"] / M_red["m00"])

		# pyautogui.moveTo(2117 + cX, 240 + cY,)
		# pyautogui.keyDown('ctrl')
		# time.sleep(0.2)
		# pyautogui.click()
		# pyautogui.keyUp('ctrl')
		# pyautogui.moveTo(2050 + cX, 240 + cY, duration=0.1)

		lock_target(cY)
		
		check_lock()

		while True:
			image = get_screenshot(Xgrid1, Ygrid1-23, Xgrid2, Ygrid2-23, hWnd)

			M_white = get_mask_moments(image, 'white')


			if(M_white["m00"] != 0):
				
				if(cnt_farm > 2):
					('unluck background or white arrows')
					break
				if(engage_target() == 0):
					cnt_farm = 0
				else:
					cnt_farm += 1

				#cd to scoop drones
				if(cd_scoop == 0):
					if(drones_hp_state()):
						cd_scoop = 12
				if(cd_scoop != 0):
					cd_scoop -= 1
				time.sleep(2)
			else:
				print('lock next target')
				time.sleep(1.5)
				break


def drop_drone():
	press_btn(0x47) # g
	time.sleep(5)
	for i in range(6):
		image = get_screenshot(XdroneMod1, YdroneMod1-23, XdroneMod2, YdroneMod2-23, hWnd)

		M_green = get_mask_moments(image, 'green')
		M_red = get_mask_moments(image, 'red')

		if((M_red["m00"] != 0) or (M_green["m00"] != 0)):
			return
		elif((M_red["m00"] == 0) and (M_green["m00"] == 0)):
			print('drones not launch')
			# clickRB(1932, 854)
			# time.sleep(0.4)
			# clickLB(1972, 866)

			press_btn(0x47) # g
			time.sleep(2)
	print('дроны не запускаются')
	exit(0)


def raise_drone():
	press_btn(0x48) # h
	for i in range(3):
		image = get_screenshot(XdroneMod1, YdroneMod1-23, XdroneMod2, YdroneMod2-23, hWnd)

		M_green = get_mask_moments(image, 'green')
		M_yellow = get_mask_moments(image, 'yellow')
		M_red = get_mask_moments(image, 'red')

		if((M_green["m00"] != 0) or (M_red["m00"] != 0)):
			if (i>=2):
				print('bad try, unluck bg, close game or bad coords')
			print('drones not comeback, attempt to raise...')
			press_btn(0x48) # h
			time.sleep(3)
		if(M_yellow["m00"] != 0):
			print('drones comeback')
			break

	for i in range(60):
		image = get_screenshot(XdroneMod1, YdroneMod1-23, XdroneMod2, YdroneMod2-23, hWnd)
		M_yellow = get_mask_moments(image, 'yellow')

		if(M_yellow["m00"] != 0):
			print('drones are still going...')
			time.sleep(2)
		else:
			print('drones are raised')
			break



### запуск функции фарма
def farm_NPC(x, y):
	print('start to farm anomalies')
	# pyautogui.moveTo(2520, raw+10)
	# time.sleep(0.5)
	# pyautogui.click()
	# time.sleep(0.5)
	clickLB(x, y-23)
	# time.sleep(0.5)

	# pyautogui.moveTo(2527, 700)
	# time.sleep(0.5)
	# pyautogui.click()
	# clickLB(2520, 677)

	check_state(5)

	date = datetime.datetime.today()
	print('бот начал фармить в: ' + date.strftime('%H:%M'))

	res_farm = check_grid()

	date = datetime.datetime.today()
	print('бот закончил фармить в: ' + date.strftime('%H:%M'))
	return res_farm


def farm_NPC_exp():
	print('start to clear sector')
	
	# check_gate()

	# check_state(5)

	check_grid()

# поиск и вывод координат строки в игре
def find_word(xw, yw, ww, hw, string):
	x, y, w, h = 0, 0, 0, 0

	image = get_screenshot(xw, yw-23, ww, hw-23, hWnd)
	
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
				(fuzz.token_set_ratio(el[11], string)) > 80
			):
				x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])
				break
		except IndexError:
			pass
			# print("Операция была пропущена")

	if (w != 0):
		print(f'{string} detected')
		y = y+int(h/2)
		return y
	print(f'{string} NOT detected')
	return False


def check_sec():
	image = get_screenshot(1200, 585-23, 1380, 610-23, hWnd)

	M_orange = get_mask_moments(image, 'orange')


	if (M_orange["m00"] != 0):
		print('low or null sec')
	else:
		print('high sec')
		return True

# открытие окна с экспой и ее поиск
def find_exp():
	clickLB(20, 135-23)
	time.sleep(1)
	clickLB(850, 1023-23)
	time.sleep(1)
	if find_word(870, 415, 985, 440, 'ESCALATIONS'):
		x = 1100
		y = 535
		while y <= 400+535:
			clickLB(x, y-23)
			y += 100
			time.sleep(0.5)
			# clickLB(1550, 933-23)
			# time.sleep(3)
			if check_sec():
				clickLB(1550, 933-23)
				time.sleep(1)
				clickLB(20, 135-23)
				time.sleep(2)
				return True
		
	clickLB(20, 135-23)
	# time.sleep(0.5)
	# clickRB(155, 348-23)
	# time.sleep(0.5)
	# clickLB(155+60, 348+126-23) # remove waypoint
	return False

# проверка открытия конта и его лут
def open_cont():
	for i in range(120):
		image = get_screenshot(XopenedCont1, YopenedCont1-23, XopenedCont2, YopenedCont2-23, hWnd)

		config = r'--oem 3 --psm 6'

		data = pytesseract.image_to_data(image, config=config)

		for i, el in enumerate(data.splitlines()):
			if i == 0:
				continue

			el = el.split()
			try:
				if(
					(fuzz.token_set_ratio(el[11], 'Cargo Container')) > 70
					# or
					# (fuzz.token_set_ratio(el[11], 'Biocombinative')) > 70
				):
					# x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])
					print('cont opened')
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

# проверка залутан ли конт
def loot_cont():
	for i in range(5):
		image = get_screenshot(XopenedCont1, YopenedCont1-23, XopenedCont2, YopenedCont2-23, hWnd)

		config = r'--oem 3 --psm 6'

		data = pytesseract.image_to_data(image, config=config)

		for i, el in enumerate(data.splitlines()):
			if i == 0:
				continue

			el = el.split()
			try:
				print(fuzz.token_set_ratio(el[11], 'Cargo Container'))
				if(
					(fuzz.token_set_ratio(el[11], 'Cargo Container')) < 70
					# or
					# (fuzz.token_set_ratio(el[11], 'Biocombinative')) > 70
				):
					# x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])
					print('cont looted')
					return
			except IndexError:
				print('cont looted')
				return
				# print("Операция была пропущена")
		clickLB(XtakeAllBtnCoords, YtakeAllBtnCoords-23) # loot
		time.sleep(4)
	print('cont NOT looted')

# запуск TAS по экспе
def run_exp():
	while go_next_exp():
		check_state_exp(10)

	clickLB(20, 135-23)
	time.sleep(1)
	clickLB(1550, 933-23)
	time.sleep(2)
	clickLB(20, 135-23)
	time.sleep(2)
	clickLB(20, 135-23)

	check_state(5)
	print('корабль прилетел в экспу')

	press_btn(0x71) # f2
	# pyautogui.press('f2')
	# time.sleep(0.25)
	# pyautogui.press('f3')

	date = datetime.datetime.today()
	print('bot start farm exp at: ' + date.strftime('%H:%M'))

	while True:
		gateAcY = find_word(XgridType1, YgridType1, XgridType2, YgridType2, 'Ancient Acceleration')
		if (gateAcY):
			clickLB(2350, 240+gateAcY-23)
			time.sleep(0.2)
			clickLB(gateCoordsX, gateCoordsY-23)
			check_state(5)

		gateAcY = find_word(XgridType1, YgridType1, XgridType2, YgridType2, 'Ancient Acceleration')
		if (gateAcY):
			clickLB(2350, 240+gateAcY-23)
			time.sleep(0.2)
			clickLB(gateCoordsX+33, gateCoordsY-23) # orbit
			press_btn(0x70) # f1
			# pyautogui.press('f1')
		else:
			break
		farm_NPC_exp()
	clickLB(2133, 232-23) # фильтр по иконкам
	time.sleep(2)
	print('check supply or telescope')
	supplY = find_word(XgridType1, YgridType1, XgridType2, YgridType2, 'Supply Radiating')
	if(supplY):
		clickLB(2245, 240+supplY-23)
		time.sleep(0.2)
		clickLB(gateCoordsX, gateCoordsY-23)
		press_btn(0x70) # f1

	farm_NPC_exp()

	supplY = find_word(XgridType1, YgridType1, XgridType2, YgridType2, 'Supply Radiating')
	if(supplY):
		clickLB(2245, 240+supplY-23)
		time.sleep(0.2)
		clickLB(gateCoordsX-66, gateCoordsY-23) # approach

	print('destroy supply or telescope')
	supplY = find_word(XgridType1, YgridType1, XgridType2, YgridType2, 'Supply Radiating')
	if(supplY):
		lock_target(supplY)
		
		press_btn(0x47) # g

		check_lock()

		engage_state()

		print('supply destroyed')

		raise_drone()

		clickLB(2133, 232-23) # фильтр по иконкам
		time.sleep(2)

		contY = find_word(Xgrid1, Ygrid1, Xgrid2, Ygrid2, 'Cargo Container')
		if contY:
			clickLB(XconstVel, YconstVel-23) # 800
			time.sleep(0.2)
			clickLB(Xgrid2, Ygrid1+contY-23)
			time.sleep(0.2)
			clickLB(gateCoordsX, gateCoordsY-23) # loot
			opened = open_cont()
			if (opened):
				time.sleep(0.5)
				loot_cont()
			time.sleep(0.5)
			clickLB(XmaxVel, YmaxVel-23) # max vel
	
	else:
		time.sleep(0.2)
		clickLB(2133, 232-23) # фильтр по иконкам
	date = datetime.datetime.today()
	print('bot end at: ' + date.strftime('%H:%M'))


# проверка локации, проверка корабля, проверка грида
date = datetime.datetime.today()
start_time = date.strftime('%H')
while (cnt_farmed < 300):

	clickLB(2360, 845)
	time.sleep(0.5)

	y = find_word(2115, 860, 2540, 1130, 'Refuge Hideaway')

	if (y):
		image = get_screenshot(XdroneMod1, YdroneMod1-23, XdroneMod2, YdroneMod2-23, hWnd)

		M_white = get_mask_moments(image, 'white')

		# calculate x,y coordinate of center
		if (M_white["m00"] != 0):
			print('refuge or Hideaway detected')
			cX = int(M_white["m10"] / M_white["m00"])
			# cY = int(M_white["m01"] / M_white["m00"])
			# print(cX, cY)

			cnt_farmed += farm_NPC(2115 + cX, 860 + y)
			print(f'зафармлено {cnt_farmed} аномалек')
			# print(f'выбито {cnt_exp} экспедиций')
		else:
			print('неточные размеры окна')
	else:
		print('there is nothing here, go next')
		go_next()
		check_state(10)
		# pyautogui.press('f2')
		clickLB(gateCoordsX-66, gateCoordsY-23) # approach
		time.sleep(1)
		press_btn(0x70) # f1
		time.sleep(0.5)
		press_btn(0x71) # f2
	date = datetime.datetime.today()
	if (abs(int(date.strftime('%H')) - int(start_time)) > 2):
		print('time to farm exp')

		while find_exp():
			run_exp()
		date = datetime.datetime.today()
		start_time = date.strftime('%H')
print('bot otrabotal')