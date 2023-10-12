import eventlet
import socketio
import json

IPS = json.load(open('IPS.json'))
IP = '172.16.50.122'
MAX_MESSAGES = 50

WEB_PATH = '/home/cedcoss/Programs/TheChat/client/views'

messages = []
try:
    messages = json.load(open("his.json")) 
except FileNotFoundError:
    pass
ips = {}
sio = socketio.Server(cors_allowed_origins="*")
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': f'{WEB_PATH}/index.html'},
    '/assets/script.js': {'content_type': 'text/javascript', 'filename': f'{WEB_PATH}/assets/script.js'},
    '/assets/style.css': {'content_type': 'text/css', 'filename': f'{WEB_PATH}/assets/style.css'},
})

@sio.event
def connect(sid, environ):
    ips[sid]=environ['REMOTE_ADDR']
    print('connect ', sid)
    sio.emit('command',{'data':{'ip':environ['REMOTE_ADDR']}},to=sid)
    sio.emit('command',{'data':{'members':list(ips.values())}})

@sio.event
def message(sid, data):
    mes={**data,'from':ips[sid],'sid':sid}
    mes['s_name'] = IPS.get(mes['from'],'None')
    messages.append(mes)
    mes['m_id'] = messages.index(mes)
    if len(messages)> MAX_MESSAGES:
        messages.pop(0)
    json.dump(messages,fp=open('his.json','w'),indent=4)
    sio.emit('message',[mes])


@sio.event
def command(sid, data):
    if data =='history':
        return messages
    if data=='members':
        return ips

@sio.event
def disconnect(sid):
    del ips[sid]
    sio.emit('command',{'data':{'members':list(ips.values())}})
    print('disconnect ', sid)

if __name__ == '__main__':
    server = eventlet.wsgi.server(eventlet.listen((IP, 51998)),app)