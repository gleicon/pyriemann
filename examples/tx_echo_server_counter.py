# twisted echo server using riemann as a hit counter

import os, sys
sys.path.append("..")
from riemann.twisted import txRiemannClient

from twisted.internet import reactor, protocol, defer

class Echo(protocol.Protocol):
    rc = txRiemannClient()

    @defer.inlineCallback
    def dataReceived(self, data):
        self.transport.write(data)
        yield rc.send({'host':'127.0.0.1', 'service': 'echo', 'state': 'hit', 'metric_f': 1})

def main():
    factory = protocol.ServerFactory()
    factory.protocol = Echo
    reactor.listenTCP(8000,factory)
    reactor.run()

if __name__ == '__main__':
    main()

