import os
import pystray
from PIL import Image
from multiprocessing import Process

image = Image.new('RGB',(256,256),'cyan')

click_callback = None

def click(icon, item):
    print(click_callback() if click_callback else 'No callback registered')


icon = pystray.Icon(name="the_chat", icon=image, title="TheChat", menu=pystray.Menu(
    pystray.MenuItem(text="Left-Click-Action",
                     action=click, default=True),
))

th = Process(target=icon.run)


def start(block=False):
    th.start()
    if block:
        th.join()


def stop():
    print('Killing tray')
    th.terminate()
    th.join()


def notify(text):
    os.system(
        f'notify-send -i {os.path.abspath("icon.jpeg")} "New message" "{text}"')


if __name__ == '__main__':
    try:
        start()
    except KeyboardInterrupt:
        stop()
