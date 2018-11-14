from __future__ import print_function
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import str
from builtins import object
try:
   from zope.interface import implementer as implements
except Exception:
   from zope.interface import implements
from twisted.internet import defer
from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.web.iweb import IBodyProducer
from twisted.web.client import Agent
from twisted.web.http_headers import Headers

from . import settings

class ResponseCruncher(Protocol):
    '''Helper for get_page()'''
    def __init__(self, finished):
        self.finished = finished
        self.response = ""

    def dataReceived(self, data):
        self.response += data

    def connectionLost(self, reason):
        self.finished.callback(self.response)

class StringProducer(object):
    '''Helper for get_page()'''
    implements(IBodyProducer)

    def __init__(self, body):
        self.body = body
        self.length = len(body)

    def startProducing(self, consumer):
        consumer.write(self.body)
        return defer.succeed(None)

    def pauseProducing(self):
        pass

    def stopProducing(self):
        pass

@defer.inlineCallbacks
def get_page(url, method='GET', payload=None, headers=None):
    '''Downloads the page from given URL, using asynchronous networking'''
    agent = Agent(reactor)

    producer = None
    if payload:
        producer = StringProducer(payload)

    _headers = {'User-Agent': [settings.USER_AGENT,]}
    if headers:
        for key, value in list(headers.items()):
            _headers[key] = [value,]

    response = (yield agent.request(
        method,
        str(url),
        Headers(_headers),
        producer))

    try:
        finished = defer.Deferred()
        (yield response).deliverBody(ResponseCruncher(finished))
    except:
        raise Exception("Downloading page '%s' failed" % url)

    defer.returnValue((yield finished))
