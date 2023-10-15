from threading import Thread
import os
import json
import time

FILE = './events.json'

if not os.path.exists(FILE):
    json.dump({},open(FILE,'w'))

def wait(func):
    try:
        recv= False
        while not recv:
            print('[watcher] still waiting')
            recv = json.load(open(FILE)).get('show',False)
            time.sleep(1)
        if callable(func):
            print(f'[watcher]  {func()}')
            return True
        else:
            print('[watcher] No callable provided')
            return False 
    except Exception as e:
        print(e)
        return False

def start(data):
    Thread(target = wait,args=[data]).start()