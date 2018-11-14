from __future__ import print_function
from __future__ import absolute_import
from builtins import object
import weakref
from twisted.internet import reactor
from .services import GenericService

class ConnectionRegistry(object):
    ''' Class to Hold a reference to each connection to an endpoint '''
    __connections = weakref.WeakKeyDictionary()

    @classmethod
    def add_connection(cls, conn):
        '''
        Add Connection to Server
        '''
        cls.__connections[conn] = True

    @classmethod
    def remove_connection(cls, conn):
        '''
        Delete Connection to Server
        '''
        try:
            del cls.__connections[conn]
        except:
            print("Warning: Cannot remove connection from ConnectionRegistry")

    @classmethod
    def get_session(cls, conn):
        '''
        Get Connection's Session Object
        '''
        if isinstance(conn, weakref.ref):
            conn = conn()

        if isinstance(conn, GenericService):
            conn = conn.connection_ref()

        if conn == None:
            return None

        return conn.get_session()

    @classmethod
    def iterate(cls):
        '''
        Return an Iterator for the connections
        '''
        return cls.__connections.iterkeyrefs()

def dump_connections():
    for x in ConnectionRegistry.iterate():
        c = x()
        c.transport.write('cus')
        print('!!!', c)
    reactor.callLater(5, dump_connections)
#reactor.callLater(0, dump_connections)
