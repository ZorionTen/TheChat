import eel
import os
import sys_tray
import json
config = json.load(open('/home/cedcoss/Programs/TheChat/client/config.json'))

print(f'PID:{os.getpid()}')

PORT = config.get('port', 51999)
PATH = config.get('views', './views')
if not os.path.exists(PATH):
    print('Views not found')
    exit(-1)
eel.init(PATH)


@eel.expose
def send_notify(text):
    sys_tray.notify(text)
    return {'value': 0, 'status': "success"}


@eel.expose
def log(text):
    print(f'[FROM EEL] {text}')
    return {'value': 0, 'status': "success"}


@eel.expose
def get_server_ip():
    return config.get('server', '0.0.0.0')

@eel.expose 
def get_hs():
    return eel.socket.gethostname()

def to_tray(a, b):
    for i in b:
        i.close()
    exit()


def from_tray():
    pass


if __name__ == '__main__':
    sys_tray.click_callback = from_tray
    sys_tray.start()
    eel.start('login.html',
              port=PORT,
              size=(1200, 800),
              #   close_callback=to_tray,
              )
    sys_tray.stop()
