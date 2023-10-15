import os
import pystray
from PIL import Image
from multiprocessing import Process

image = Image.new('RGB',(256,256),'cyan')

click_callback = None

def click(icon, item):
    print('[TRAY CALLBACK]---')
    print(click_callback() if click_callback else 'No callback registered')
    print('[TRAY CALLBACK]---')


icon = pystray.Icon(name="the_chat", icon=image, title="TheChat", menu=pystray.Menu(
    pystray.MenuItem(text="Left-Click-Action",
                     action=click, default=True),
))

def start(block=False):
    icon.run if block else icon.run_detached() 


def stop():
    print('Killing tray')
    icon.stop()


def notify(text):
    os.system(
        f'notify-send -i {os.path.abspath("icon.jpeg")} "TheChat" "{text}"')


if __name__ == '__main__':
    try:
        start()
    except KeyboardInterrupt:
        stop()
