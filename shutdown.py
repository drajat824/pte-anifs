import pigpio
import time
import os

pi = pigpio.pi()
BUTTON_PIN = 26
pi.set_mode(BUTTON_PIN, pigpio.INPUT)

def shutdown_raspberry():
    print("Shutting down...")
    time.sleep(1)
    os.system("sudo shutdown -h now")

try:
    while True:
        button_state = pi.read(BUTTON_PIN)
        if button_state == 1:
            shutdown_raspberry()
            break
        time.sleep(0.1)
finally:
    pi.stop()