import asyncio
import desktop_notifier as dn
import desktop_notifier.resources as dnr
import os
os.environ['PYSTRAY_BACKEND'] = 'xorg'
from pystray import Icon as icon, Menu as menu, MenuItem as item
from PIL import Image, ImageDraw
from threading import Thread

ICON_PATH = 'views/favicon.png'
notifier = dn.DesktopNotifier()
def_icon = None
noti_icon = None
_icon = None
click_callback = None
loop = None

def start_loop():
    global loop
    try:
        loop = asyncio.get_event_loop() 
    except RuntimeError:
        loop = asyncio.new_event_loop()
    loop.run_forever()

def get_image():
    global def_icon
    if not def_icon:
        def_icon = Image.open(ICON_PATH)
    return def_icon


def get_dot_image(path=ICON_PATH):
    global noti_icon
    if not noti_icon:
        image = Image.open(path)
        draw = ImageDraw.Draw(image)
        dot_radius = image.size[0]//2  # Change this to the desired size
        dot_position = (image.size[0], image.size[1])  # Change this to the desired position
        dot_color = (255, 0, 0)
        draw.ellipse([dot_position[0] - dot_radius, dot_position[1] - dot_radius,
                      dot_position[0] + dot_radius, dot_position[1] + dot_radius],
                     fill=dot_color)
        noti_icon = image
    return noti_icon

def stop():
    Thread(target=_icon.stop).start()
def call():
    _icon.icon = get_image() 
    click_callback() if click_callback else print('No callback')


async def create_notify(text):
    await notifier.send(
        title="TheChat - New Message",
        message=text,
        on_clicked=lambda: call(),
        on_dismissed=lambda: print("Notification dismissed"),
        sound=True,
    )

def notify(text):
    _icon.icon=get_dot_image(ICON_PATH)
    asyncio.run_coroutine_threadsafe(create_notify(text),loop)

def make_icon():
    return icon('TheChat',
        icon=get_image(),menu=menu(item('restore',call,default=True)))

def start():
    global _icon
    Thread(target=start_loop).start()
    _icon=make_icon()
    _icon.run_detached()
        


if __name__ == '__main__':
    print(f'kill -9 {os.getpid()}')
    ICON_PATH = "/home/zaid-1942/Programs/TheChat/client/views/favicon.png"
    # get_dot_image().save('./tmp.png')
    start()
    notify('33')
    try:
        while True:
            asyncio.sleep(1)
    except KeyboardInterrupt:
        exit(0)