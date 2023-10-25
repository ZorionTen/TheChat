import os

ICON_PATH = 'anydesk'

def notify(text):
    os.system(f'notify-send -i {ICON_PATH} "TheChat - Alert" "{text}"')

if __name__ == '__main__':
    notify("test")
