import keyboard
import time


def stopkeyboard(x):
    for i in range(150):
        keyboard.block_key(i)
    time.sleep(x * 60)

stopkeyboard(1)
print("TEst")