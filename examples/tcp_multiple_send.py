import os, sys
sys.path.append("..")
from riemann import RiemannClient
from riemann.gevent_transport import RiemannGEventTCPTransport
import time

def main():
    rc = RiemannClient()
    tb = time.time()

    for n in xrange(100):
        rc.send({'host':'127.0.0.1', 'service': 'www%d' % n, 'state': 'down', 'metric_f': 10000})
    
    print time.time() - tb

    res = rc.query('service')
    print res
    if res is not None:
        for e in res.events: print e.host


if __name__ == '__main__':
    main()

