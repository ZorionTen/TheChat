import webview as wv
import os
import sys_tray
import json
import watcher
import socket
import sys

try:
    BASE_PATH = sys._MEIPASS
except AttributeError:
    BASE_PATH = '.'
print(BASE_PATH)
try:
    config = json.load(open(BASE_PATH+'/config.json'))
except FileNotFoundError:
    print('[ERROR] config.json not found, Loading defaults')
    config = {'server': '172.16.50.122'}

print(f'kill -9 {os.getpid()}')

PORT = config.get('port', 51999)
PATH = config.get('views', BASE_PATH+'/views')
if not os.path.exists(PATH):
    print('Views not found')
    exit(-1)

window = None


class Api:
    def __init__(self, window=None):
        if window:
            self.window = window
        self.kill_flag = False
        self.hidden=False

    def send_notify(self, text):
        print(f'hidden {self.hidden}')
        if self.hidden:
            sys_tray.notify(text)

    def log(self, text):
        print(f'[FROM PY_CLIENT] {text}')

    def get_server_ip(self):
        return config.get('server', '0.0.0.0')

    def get_hs(self):
        # ToDO: find a better way
        return socket.gethostname()

    def to_tray(self):
        if self.kill_flag:
            return True
        if self.window:
            self.window.hide()
        watcher.start(self.from_tray)
        self.hidden = True
        return False

    def from_tray(self):
        if self.window:
            self.window.show()
        json.dump({}, open(watcher.FILE, 'w'))
        self.hidden = False
        return 200

    def quit(self):
        self.kill_flag = True
        self.window.destroy()


def fire_open():
    json.dump({"show": 1}, open(watcher.FILE, "w"))


api = Api()
window = wv.create_window(
    title='TheChat', transparent=True, background_color = '#202020',url=f'{PATH}/login.html', js_api=api,
    min_size=(1200, 800))
api.window = window
# Register events
window.events.closing += api.to_tray

if __name__ == '__main__':
    print(f'Starting server on port {PORT}')
    print(f'Serving files at {PATH}')
    sys_tray.click_callback = fire_open
    sys_tray.start()
    wv.start(debug=False)
    sys_tray.stop()
