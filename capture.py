import ctypes
from time import sleep
import pyautogui
import yaml

with open('./settings.yml') as f:
    settings = yaml.safe_load(f)
PAGES = settings['CAPTURE']['PAGES']
SLEEP_TIME = settings['CAPTURE']['SLEEP_TIME']

# 画面固定化
pyautogui.hotkey('alt', 'tab')

# 座標取得
sleep(1)
pyautogui.alert("キャプチャしたい左上をクリック")
while True:
    if ctypes.windll.user32.GetAsyncKeyState(0x01) == 0x8000:
        start_point = pyautogui.position()
        break
sleep(1)
pyautogui.alert("キャプチャしたい右下をクリック")
print(f"start: {start_point}")
while True:
    if ctypes.windll.user32.GetAsyncKeyState(0x01) == 0x8000:
        end_point = pyautogui.position()
        break
print(f"end: {end_point}")

# 待機
pyautogui.alert("5秒後にスタートします")
sleep(5)

for index in range(PAGES):
    screenshot = pyautogui.screenshot(region=(
        start_point[0],
        start_point[1],
        end_point[0] - start_point[0],
        end_point[1] - start_point[1],
    ))
    screenshot.save(f'outputs_main/{index+1:0>4}.png')
    pyautogui.press('right')
    sleep(SLEEP_TIME)

pyautogui.alert("---END---")
