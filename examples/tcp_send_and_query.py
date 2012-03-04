import os, sys
sys.path.append("..")
from riemann import RiemannClient

def main():
    rc = RiemannClient()
    rc.send({'host':'127.0.0.1', 'service': 'www', 'state': 'down', 'metric_f': 10000})
    res = rc.query('host')
    print res
    for e in res.events: print e.host


if __name__ == '__main__':
    main()

