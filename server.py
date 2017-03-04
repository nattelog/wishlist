from flask import Flask, request
from flask_socketio import SocketIO, send
from wishlist import Wishlist
import json

app = Flask(__name__)
socketio = SocketIO(app)
wishlist = Wishlist()

# Request handler

def send_response(response, sid):
  print 'sending {}'.format(response)
  send(response, json=True, room=sid)

def process_request(request, sid):
  try:
    data = json.loads(request)
    method = data['method']
    args = data['args']

    print 'calling {} with {}'.format(method, args)

    result = getattr(wishlist, method)(*args)
    send_response({ 'result': result }, sid)
  except Exception as e:
    send_response({
      'error': {
        'name': type(e).__name__,
        'args': e.args
      }
    }, sid)

# API

@socketio.on('message')
def on_message(message):
  sid = request.sid
  process_request(message, sid)

if __name__ == '__main__':
  socketio.run(app)
