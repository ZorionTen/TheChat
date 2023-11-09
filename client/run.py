import client
import os
import sys
from PySide2.QtWidgets import QApplication, QMessageBox
import subprocess
from multiprocessing import Process
import time

FILE = os.path.dirname(__file__)+'/instance'

def show_alert(text):
    QApplication(sys.argv)
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(text)
    msg.setWindowTitle("TheChat")
    msg.exec_()
    return msg


def main():
    if os.path.exists(FILE):
        kill_cmd = ""
        with open(FILE) as f:
            kill_cmd = f.read()
        show_alert(f'An instance is already running\nkill using: {kill_cmd}')
    else:
        with open(FILE, 'w') as f:
            f.write(f'kill -9 {os.getpid()}')
        client.main()
        os.unlink(FILE)


def update_client():
    file_path = os.environ['HOME']+'/.TheChat/src'
    os.chdir(file_path)
    result = subprocess.run(
        ['git', 'pull'], stdout=subprocess.PIPE).stdout.decode()
    print(result)


if __name__ == "__main__":
    try: 
        th = Process(target = show_alert,args=('Updating app',))
        th.start()
        update_client()
        th.terminate()
        main()
    except Exception as e:
        print('Exiting gracefully')
        if os.path.exists(FILE):
            os.unlink(FILE)
        print(e)
        raise e
    finally:
        time.sleep(10)
        os.system(f'kill -9 {os.getpid()}')
