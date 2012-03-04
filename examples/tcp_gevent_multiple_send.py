import os, sys
sys.path.append("..")
from riemann import RiemannClient
import time
import gevent
from gevent import pool
from gevent import monkey
gevent.monkey.patch_all()

def _s(pars):
    rc = RiemannClient()
    r = rc.send(pars)
    # do something with r

def main():
    tb = time.time()
    p = pool.Group()

    for n in xrange(100):
        pars = {'host':'127.0.0.1', 'service': 'www%d' % n, 'state': 'down', 'metric_f': 10000}
        c = p.spawn(_s, pars)
    
    p.join()

    print time.time() - tb


if __name__ == '__main__':
    main()

