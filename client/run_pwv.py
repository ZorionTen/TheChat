import webview as wv
import sys
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

window = None


class Api:
    def send_notify(self, text):
        sys_tray.notify(text)
        return {'value': 0, 'status': "success"}

    def log(self, text):
        print(f'[FROM EEL] {text}')
        return {'value': 0, 'status': "success"}

    def get_server_ip(self):
        return config.get('server', '0.0.0.0')

    def get_hs(self):
        return 'polymouth'

    def to_tray(self):
        if window:
            window.destroy()

    def from_tray(self):
        if window:
            window.show()


def closing():
    print('Sent to tray')
    window.hide()
    return False


api = Api()
window = wv.create_window(
    title='TheChat', url=f'{PATH}/login.html', js_api=api,
    min_size=(1200, 800))

# Register events
window.events.closing += closing

if __name__ == '__main__':
    print(f'Starting server on port {PORT}')
    print(f'Serving files at {PATH}')
    sys_tray.click_callback = api.from_tray
    sys_tray.start()
    wv.start(debug=False)
    sys_tray.stop()
