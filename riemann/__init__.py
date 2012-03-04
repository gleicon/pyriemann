import pb.proto_pb2 as pb
import socket
import struct

class RiemannUDPTransport():
    def __init__(self, host='127.0.0.1', port=5555):
        self._host = host
        self._port = port
    
    def write(self, buffer): # needs cleanup, conn pool
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(buffer, (self._host, self._port))
        sock.close()

class RiemannTCPTransport():
    def __init__(self, host='127.0.0.1', port=5555):
        self._host = host
        self._port = port
    
    def write(self, buffer):
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

class RiemannClient():
    """
    Client to Riemann. 
    RiemannClient constructor can receive the following parameters:
    - host
    - port
    - transport (RiemannUDPTransport, RiemannTCPTransport or any class that
      implements the write() method and receive both host and port on __init__())

    Example: 
    from riemann import RiemannClient

    rc = RiemannClient()
    rc.send({'host':'127.0.0.1', 'service': 'www', 'state': 'down', 'metric_f': 10000})
    res = rc.query('host')
    print res
    for e in res.events: print e.host
    """
    def __init__(self, host='127.0.0.1', port=5555, transport=RiemannTCPTransport):
        self._fields = ['description', 'host', 'metric_f', 'service', 'state', 'tags', 'time', 'ttl']
        self._host = host
        self._port = port
        self._transport = transport(host=host, port=port)

    def send(self, edict):
        ev = pb.Event()
        for k in self._fields:
            if edict.has_key(k): setattr(ev, k, edict[k]) 
        msg = pb.Msg()
        msg.events.extend([ev])
        b = msg.SerializeToString()
        return self._transport.write(b)

    def query(self, query):
        msg = pb.Msg()
        msg.query.string = str(query)
        return self._transport.write(msg.SerializeToString())
