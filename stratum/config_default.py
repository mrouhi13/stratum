'''
This is example configuration for Stratum server.
Please rename it to config.py and fill correct values.
'''

# ******************** GENERAL SETTINGS ***************

# Enable some verbose debug (logging requests and responses).
DEBUG = True

# Destination for application logs, files rotated once per day.
LOGDIR = 'log/'

# Main application log file.
LOGFILE = None #'stratum.log'

# Possible values: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOGLEVEL = 'DEBUG'

# How many threads use for synchronous methods (services).
# 30 is enough for small installation, for real usage
# it should be slightly more, say 100-300.
THREAD_POOL_SIZE = 300

# Do you want to expose "example" service in server?
# Useful for learning the server,you probably want to disable
# this on production
ENABLE_EXAMPLE_SERVICE = True

# ******************** TRANSPORTS *********************

# Hostname or external IP to expose
HOSTNAME = 'localhost'

# Port used for Socket transport. Use 'None' for disabling the transport.
LISTEN_SOCKET_TRANSPORT = None

# Port used for HTTP Poll transport. Use 'None' for disabling the transport
LISTEN_HTTP_TRANSPORT = None

# Port used for HTTPS Poll transport
LISTEN_HTTPS_TRANSPORT = None

# Port used for WebSocket transport, 'None' for disabling WS
LISTEN_WS_TRANSPORT = None

# Port used for secure WebSocket, 'None' for disabling WSS
LISTEN_WSS_TRANSPORT = None

# ******************** SSL SETTINGS ******************

# Private key and certification file for SSL protected transports
# You can find howto for generating self-signed certificate in README file
SSL_PRIVKEY = ''
SSL_CACERT = ''

# ******************** TCP SETTINGS ******************

# Enables support for socket encapsulation, which is compatible
# with haproxy 1.5+. By enabling this, first line of received
# data will represent some metadata about proxied stream:
# PROXY <TCP4 or TCP6> <source IP> <dest IP> <source port> </dest port>\n
#
# Full specification: http://haproxy.1wt.eu/download/1.5/doc/proxy-protocol.txt
TCP_PROXY_PROTOCOL = False

# ******************** HTTP SETTINGS *****************

# Keepalive for HTTP transport sessions (at this time for both poll and push)
# High value leads to higher memory usage (all sessions are stored in memory ATM).
# Low value leads to more frequent session reinitializing (like downloading address history).
HTTP_SESSION_TIMEOUT = 3600 # in seconds

# Maximum number of messages (notifications, responses) waiting to delivery to HTTP Poll clients.
# Buffer length is PER CONNECTION. High value will consume a lot of RAM,
# short history will cause that in some edge cases clients won't receive older events.
HTTP_BUFFER_LIMIT = 10000

# User agent used in HTTP requests (for both HTTP transports and for proxy calls from services)
USER_AGENT = 'Stratum/0.1'

# Provide human-friendly user interface on HTTP transports for browsing exposed services.
BROWSER_ENABLE = True

# Use "./signature.py > signing_key.pem" to generate unique signing key for your server
SIGNING_KEY = '' # Message signing is disabled

# Origin of signed messages. Provide some unique string,
# ideally URL where users can find some information about your identity
SIGNING_ID = HOSTNAME # Use hostname as the signing ID

# *********************** IRC / PEER CONFIGURATION *************

IRC_NICK = None # Skip IRC registration

# Which hostname / external IP expose in IRC room
# This should be official HOSTNAME for normal operation.
IRC_HOSTNAME = HOSTNAME

# Don't change this unless you're creating private Stratum cloud.
IRC_SERVER = 'irc.freenode.net'
IRC_ROOM = '#stratum'
IRC_PORT = 6667

