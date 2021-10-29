from selenium import webdriver
import time
import pyautogui
import base64
import io
from PIL import Image

driver_path = "C:\Programacion\chromedriver.exe"
driver = webdriver.Chrome(executable_path=driver_path)

driver.get('https://www.trex-game.skipser.com/')


def check_img():
    canvas = driver.find_element_by_xpath('//*[@id="gamecanvas"]')

    # get the canvas as a PNG base64 string
    canvas_base64 = driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);", canvas)

    # decode
    canvas_png = base64.b64decode(canvas_base64)

    image = Image.open(io.BytesIO(canvas_png))

    # Check if pixels turn black
    rgb_im = image.convert('RGB')

    # Check multiple x position for more accuracy
    list_of_rgbs = []
    for n in range(50, 80):
        list_of_rgbs.append(rgb_im.getpixel((n, 120)))
        list_of_rgbs.append(rgb_im.getpixel((n, 95)))

    for l in list_of_rgbs:
        if l[0] == 247:
            return True

    # Check game over
    r, g, b = rgb_im.getpixel((322, 45))
    if r == 247:
        return "Restart"

    else:
        return False


# Start Game
time.sleep(2)
pyautogui.press('space')

game_on = True
while game_on:

    if check_img():
        pyautogui.press('space')

    if check_img() == "Restart":
        time.sleep(1)
        pyautogui.press('space')
