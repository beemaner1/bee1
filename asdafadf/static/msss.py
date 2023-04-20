from mss import mss
import time

while True:
    mss().shot(mon=1)
    time.sleep(0.1)
