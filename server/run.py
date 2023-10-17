import eventlet
import socketio
import json
import time
from datetime import datetime ,timedelta
from tinydb import TinyDB, Query, where
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware

IP = '0.0.0.0'
MAX_MESSAGES = 50

## TODO: make web app
# WEB_PATH = '/home/cedcoss/Programs/TheChat/client/views'

DB = TinyDB('./database/messages.json',storage=CachingMiddleware(JSONStorage))
query = Query()

messages = DB.table('messages') 
ips = {}
sio = socketio.Server(cors_allowed_origins="*")
app = socketio.WSGIApp(sio)

def delete_old_messages():
    cutoff_time = datetime.now() - timedelta(days=1)

    # Find documents older than a day
    old_entries = messages.search((query.sat < cutoff_time.timestamp()))

    # Delete the old entries
    for entry in old_entries:
        messages.remove(query.sat == entry['sat'])

###
# SERVER
###
@sio.event
def connect(sid, environ):
    ips[sid]=environ['REMOTE_ADDR']
    print('connect ', sid)
    sio.emit('command',{'data':{'ip':environ['REMOTE_ADDR']}},to=sid)
    sio.emit('command',{'data':{'members':list(ips.values())}})

@sio.event
def message(sid, data):
    mes={**data,'from':ips[sid],'sid':sid,'sat':time.time(),'uid':f'{sid}_{int(time.time())}'}
    messages.insert(mes)
    sio.emit('message',[mes])


@sio.event
def command(sid, data):
    if data =='history':
        delete_old_messages()
        results = messages.search(query.sat.exists())
        results.sort(key=lambda x: x['sat'],reverse=False)
        return results[:50]
    if data=='members':
        return ips


@sio.event
def edit(sid,data):
    sio.emit('edited',{'uid':data['uid'],"text":data['text']})
    return {'response':messages.update({'text':data['text']},Query().uid==data['uid'])}


@sio.event
def delete(sid, data):
    sio.emit('deleted', {'uid': data['uid']})
    return {'response': messages.remove(where('uid')==data['uid'])}

@sio.event
def disconnect(sid):
    del ips[sid]
    sio.emit('command',{'data':{'members':list(ips.values())}})
    print('disconnect ', sid)

if __name__ == '__main__':
    try:
        server = eventlet.wsgi.server(eventlet.listen((IP, 51998)),app)
    except Exception as e:
        print(e)
    finally:
        DB.close()