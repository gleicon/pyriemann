#!/usr/bin/env python
"""
Send events to Riemann from CLI

"""

from riemann import RiemannClient
import argparse
import socket
import time

def main():
  parser = argparse.ArgumentParser(description='Send events to Riemann.')
  parser.add_argument('-r', '--riemann', dest='rie_host', action='store',
                      type=str, required=True,
                      help='IP/hostname for Riemann server')
  parser.add_argument('-R', '--riemann-port', dest='rie_port', action='store',
                      type=int, default=5555,
                      help='IP/hostname for Riemann server')

  parser.add_argument('-H', '--host', dest='evt_host', action='store',
                      type=str, default=socket.getfqdn(),
                      help='Hostname for event')
  parser.add_argument('-s', '--service', dest='evt_service', action='store',
                      type=str, help='Service for event')
  parser.add_argument('-S', '--state', dest='evt_state', action='store',
                      type=str, help='Current state for event')
  parser.add_argument('-T', '--time', dest='evt_time', action='store',
                      type=int, default=int(time.time()),
                      help='Timestamp for event')

  parser.add_argument('-a', '--attribute', dest='evt_attrib', action='append',
                      type=str, help='Event attribute (key=value), multiple allowed')
  parser.add_argument('-d', '--description', dest='evt_description',
                      action='store', type=str, help='Event description')
  parser.add_argument('-t', '--tags', dest='evt_tags', action='append',
                      type=str, help='Event tags, multiple allowed')
  parser.add_argument('-m', '--metric', dest='evt_metric', action='store',
                      type=float, help='Event metric')
  parser.add_argument('--ttl', dest='evt_ttl', action='store', type=int,
                      default=60, help='Event TTL')
  args = parser.parse_args()


  event = {}
  for i in ['host', 'service', 'time', 'description', 'tags', 'metric', 'ttl']:
    if getattr(args, 'evt_' + i):
      event[i] = getattr(args, 'evt_' + i)

  if getattr(args, 'evt_attrib', None):
    event['attributes'] = dict(item.split('=') for item in getattr(args, 'evt_attrib'))

  print(repr(event))

  rc = RiemannClient(host=args.rie_host, port=args.rie_port)
  rc.send(event)

if __name__ == '__main__':
  main()


