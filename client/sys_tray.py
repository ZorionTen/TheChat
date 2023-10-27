import asyncio
import desktop_notifier as dn
import desktop_notifier.resources as dnr
import os
os.environ['PYSTRAY_BACKEND'] = 'xorg'
from pystray import Icon as icon, Menu as menu, MenuItem as item
from PIL import Image, ImageDraw
from threading import Thread

ICON_PATH = 'views/favicon.ico'
notifier = dn.DesktopNotifier()
def_icon = None
noti_icon = None
_icon = None
click_callback = None


def get_image():
    global def_icon
    if not def_icon:
        def_icon = Image.open(ICON_PATH)
    return def_icon


def get_dot_image(path):
    global noti_icon
    if not noti_icon:
        image = Image.open(path)
        draw = ImageDraw.Draw(image)
        dot_position = (50, 50)  # Change this to the desired position
        dot_radius = 5  # Change this to the desired size
        dot_color = (255, 0, 0)
        draw.ellipse([dot_position[0] - dot_radius, dot_position[1] - dot_radius,
                      dot_position[0] + dot_radius, dot_position[1] + dot_radius],
                     fill=dot_color)
        noti_icon = image
    return noti_icon


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
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_notify(text))
    loop.close()
    _icon.icon = get_dot_image(ICON_PATH)
    # os.system(f'notify-send -i {ICON_PATH} "TheChat - Alert" "{text}"')

def start():
    global _icon
    _icon = icon(
        'TheChat',
        icon=get_image())
    _icon.run_detached()
    # Thread(target=loop.run_forever).start()


if __name__ == '__main__':
    notify('TEST')
