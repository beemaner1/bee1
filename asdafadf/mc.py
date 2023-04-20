import webbrowser, ctypes, time, os

os.system("pip install pynput")
import pynput

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)

print(screensize)

for i in range(0, 10):
    webbrowser.open("https://www.youtube.com/watch?v=YRvOePz2OqQ")

    t = time.time()
    print(t)
    while True:
        pynput.mouse.Controller().position = screensize[0] / 4, screensize[1] / 4
        if (time.time() - t) >= 4 and (time.time() - t) <= 5:
            pynput.mouse.Controller().press(pynput.mouse.Button.left)
            time.sleep(0.1)
            pynput.mouse.Controller().release(pynput.mouse.Button.left)
            break

    time.sleep(1)


