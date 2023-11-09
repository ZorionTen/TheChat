import client
import os
import sys
from PySide2.QtWidgets import QApplication, QMessageBox

FILE = os.path.dirname(__file__)+'/instance'
def show_alert(text):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(text)
    msg.setWindowTitle("TheChat")
    msg.exec_()

def main():
    if os.path.exists(FILE):
        kill_cmd = ""
        with open(FILE) as f:
            kill_cmd=f.read()
        app = QApplication(sys.argv)
        show_alert(f'An instance is already running\nkill using: {kill_cmd}')
    else:
        with open(FILE,'w') as f:
            f.write(f'kill -9 {os.getpid()}')
        client.main()
        os.unlink(FILE)

if __name__=="__main__":
    try:
        main()
    except Exception as e:
        print('Exiting gracefully')
        if os.path.exists(FILE):
            os.unlink(FILE)
        raise e
    finally:
        os.system(f'kill -9 {os.getpid()}')