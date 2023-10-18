import os
import pystray
from PIL import Image
import sys

try:
    BASE_PATH = sys._MEIPASS
except AttributeError:
    BASE_PATH = os.path.dirname(__file__)

image = Image.open(BASE_PATH+'/views/favicon.ico')

click_callback = None


def click(icon, item):
    print('[TRAY CALLBACK]---')
    print(click_callback() if click_callback else 'No callback registered')
    print('[TRAY CALLBACK]---')

def start(block=False):
    icon.run() if block else icon.run_detached()


def stop():
    print('Killing tray')
    os.system(f'kill -9 {os.getpid()}')
    icon.stop()


def notify(text):
    os.system(
        f'notify-send -i {BASE_PATH+"/views/favicon.ico"} "TheChat" "{text}"')


icon = pystray.Icon("TC", image, "TheChat", menu=pystray.Menu(
    pystray.MenuItem("??", click, default=True),
    pystray.MenuItem("Restore", click),
    pystray.MenuItem("Quit", stop),
))


if __name__ == '__main__':
    try:
        start()
    except KeyboardInterrupt:
        stop()
