import eel
import os
import sys_tray
import time
import sys

print(f'PID:{os.getpid()}')

PORT = 51999
PATH = '/home/zorionten/Programs/webChat/client/views'

eel.init(PATH)


@eel.expose
def send_notify(text):
    sys_tray.notify(text)
    return {'value': 0, 'status': "success"}

@eel.expose
def log(text):
    print(f'[FROM EEL] {text}')
    return {'value': 0, 'status': "success"}


def to_tray(a, b):
    for i in b:
        i.close()
    exit()


def from_tray():
    eel.show(f'http://localhost:{PORT}')


if __name__ == '__main__':
    sys_tray.click_callback=from_tray
    sys_tray.start()
    eel.start('index.html',
              port=PORT,
              size=(1600, 800),
              block=True,
              )
    # while True:
    #     eel.sleep(1)
    sys_tray.stop()
