import keyboard
import time
a = int(input("Enter the time (in seconds) for which you want to disable keyboard: "))
for i in range(150):
    keyboard.block_key(i)
time.sleep(a)
