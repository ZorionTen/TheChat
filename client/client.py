import requests
import sys
import socket
import watcher
import json
import sys_tray
import os
import webview as wv
from webview.util import environ_append
environ_append("QTWEBENGINE_CHROMIUM_FLAGS", "--no-sandbox", "--no-sandbox")

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
        self.hidden = False

    def send_notify(self, text):
        if self.hidden:
            sys_tray.notify(text)

    def log(self, text):
        print(f'[JS>PY] {text}')

    def get_server_ip(self):
        return config.get('server', '0.0.0.0')

    def get_hs(self):
        # ToDO: find a better way
        return socket.gethostname()

    def to_tray(self):
        if self.kill_flag:
            return True
        if self.window:
            self.window.minimize()
        self.hidden = True
        return False

    def from_tray(self):
        self.hidden = False
        if self.window:
            self.window.restore()
        return 200

    def quit(self):
        os.system(f"kill -9 {os.getpid()}")
        self.kill_flag = True
        self.window.destroy()

    def update_client(self, url):
        file_path = os.environ['HOME']+'/.TheChat/client'
        if os.path.exists(file_path):
            old_file_path = f"{file_path}.old"
            os.rename(file_path, old_file_path)
            print(f"Renamed {file_path} to {old_file_path}")
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_path, 'wb') as new_file:
                new_file.write(response.content)
            print(f"Downloaded and saved new file to {file_path}")
        else:
            print(f"Failed to download the file from {url}")


def fire_open():
    json.dump({"show": 1}, open(watcher.FILE, "w"))


api = Api()
window = wv.create_window(
    title='TheChat', transparent=True, background_color='#202020', url=f'{PATH}/login.html', js_api=api,
    min_size=(1600, 800))
api.window = window
# Register events
window.events.closing += api.to_tray
window.events.restored += api.from_tray

if __name__ == '__main__':
    print(f'Starting server on port {PORT}')
    print(f'Serving files at {PATH}')
    sys_tray.ICON_PATH = PATH+'/favicon.ico'
    sys_tray.click_callback = api.from_tray
    sys_tray.start()
    wv.start(debug='--dev' in sys.argv, http_server=True)
