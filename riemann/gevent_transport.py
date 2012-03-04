import pb.proto_pb2 as pb
import struct
import gevent
from gevent import socket
from gevent import monkey

monkey.patch_all()

class RiemannGEventUDPTransport():
    def __init__(self, host='127.0.0.1', port=5555):
        self._host = host
        self._port = port

    def write(self, buffer):
        gevent.spawn(self._write, buffer)

    def _write(self, buffer):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(buffer, (self._host, self._port))
        sock.close()

class RiemannGEventTCPTransport():
    def __init__(self, host='127.0.0.1', port=5555):
        self._host = host
        self._port = port

    def write(self, buffer):
        gevent.spawn(self._write, buffer)

    def _write(self, buffer):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        sock.connect((self._host,self._port))
        l = len(buffer)
        hdr = struct.pack('!I', l)
        sock.send(hdr)
        sock.send(buffer)
        r = sock.recv(4)
        hl = struct.unpack('!I', r)
        res = sock.recv(hl[0])
        c = pb.Msg().FromString(res)
        sock.close()
        return c
