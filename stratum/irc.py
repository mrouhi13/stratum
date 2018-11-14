from __future__ import absolute_import
from builtins import range
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol, defer
import random
import string

from . import custom_exceptions
from . import logger
log = logger.get_logger('irc')

# Reference to open IRC connection
_connection = None

def get_connection():
    if _connection:
        return _connection
    raise custom_exceptions.IrcClientException("IRC not connected")

class IRCClient(irc.IRCClient):
    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        self.peers = {}

        global _connection
        _connection = self

    def get_peers(self):
        return list(self.peers.values())

    def connectionLost(self, reason):
        print(reason)
        irc.IRCClient.connectionLost(self, reason)

        global _connection
        _connection = None

    def signedOn(self):
        self.join(self.factory.channel)

    def joined(self, channel):
        log.info('Joined %s' % channel)

    def _sendMessage(self, msg, target, nick=None):
        if not msg:
           return
        if nick:
            msg = '%s, %s' % (nick, msg)
        self.msg(target, msg)

    def _showError(self, failure):
        log.error(failure)
        return failure.getErrorMessage()

    def register(self, nickname, *args, **kwargs):
        self.setNick(nickname)
        self.sendLine("USER %s 0 * :%s" % (self.nickname, self.factory.hostname))

    def userJoined(self, nickname, channel):
        self.sendLine("WHO %s" % nickname)

    def userLeft(self, nickname, channel):
        self.userQuit(nickname)

    def userKicked(self, nickname, *args, **kwargs):
        self.userQuit(nickname)

    def userQuit(self, nickname, *args, **kwargs):
        try:
            hostname = self.peers[nickname]
            del self.peers[nickname]
            log.info("Peer '%s' (%s) disconnected" % (hostname, nickname))
        except:
            pass

class IRCClientFactory(protocol.ClientFactory):
    protocol = IRCClient

    def __init__(self, channel, nickname, hostname):
        self.channel = channel
        self.nickname = nickname
        self.hostname = hostname

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        log.error("Connection lost %s", reason)
        reactor.callLater(10, connector.connect)

    def clientConnectionFailed(self, connector, reason):
        log.error("Connection failed %s", reason)
        reactor.callLater(10, connector.connect)

if __name__ == '__main__':
    # Example of using IRC bot
    reactor.connectTCP("irc.freenode.net", 6667, IRCClientFactory('#stratum-nodes', 'test', 'example.com'))
    reactor.run()
