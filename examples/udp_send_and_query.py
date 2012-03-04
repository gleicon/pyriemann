import os, sys
sys.path.append("..")
from riemann import RiemannClient, RiemannUDPTransport

def main():
    rc = RiemannClient(transport = RiemannUDPTransport)
    rc.send({'host':'127.0.0.1', 'service': 'www', 'state': 'down', 'metric_f': 10000})
    # all responses are None for udp.

if __name__ == '__main__':
    main()

