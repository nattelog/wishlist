import threading
import socket


class Request(threading.Thread):

  def __init__(self, owner, conn):
    threading.Thread.__init__(self)
    self.owner = owner
    self.conn = conn


  def process_request(self, request):
    print 'processing request: {}'.format(request)
    return 'Hello!'


  def run(self):
    try:
      worker = self.conn.makefile(mode='rw')
      request = worker.readline()
      result = self.process_request(request)
      worker.write(result + '\n')
      worker.flush()
    except Exception as error:
      print 'The socket died:'
      print '\t{}: {}'.format(type(e), e)


class Skeleton():

  def __init__(self, owner, address):
    # threading.Thread.__init__(self)
    self.owner = owner
    self.address = address
    self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server.bind(self.address)
    self.server.listen(5)


  def start(self):
    while True:
      try:
        conn, addr = self.server.accept()

        print 'connection from {}'.format(addr)

        req = Request(self.owner, conn)
        req.start()

      except socket.error:
        print socket.error
        continue
