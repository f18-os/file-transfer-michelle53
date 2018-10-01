#! /usr/bin/env python3
# File Client program

import sys
sys.path.append( '../lib' ) # for params
import socket, re, params

switchesVarDefaults = ( ( ( '-s', '--server' ), 'server', ' 127.0.0.1:50001' ), ( ( '-?', '--usage'), 'usage', False ),  )



progname = 'fileClient'
paramMap = params.parseParams( switchesVarDefaults )

server, usage = paramMap[ 'server' ], paramMap[ 'usage' ]

if usage:
    param.usage()

try:
    serverHost, serverPort = re.split( ':', server )
    serverPort = int( serverPort )
except:
    print( 'Cannot parse server: port from %s' % server )
    sys.exit( 1 )


s = None

for res in socket.getaddrinfo( serverHost, serverPort, socket.AF_UNSPEC, socket. SOCK_STREAM ):
    af,socktype, proto, cannonname, sa = res
    try:
        print('creating sock: af=' + af + ', type=' + socktype + ', proto=' + proto)
        s = socket.socket( af, socktype, proto )

    except socket.error as msg:
        print( 'error: ' + msg )
        continue
    try:
        print('attempting connection to ' + repr( sa ) )
        s.connect( sa )
    except socket.error as msg:
        print( 'error: ' + msg )
        s.close( )
        s = None
        continue

    break

if s is None:
    print( ' Socket could not be opnened! ' )
    sys.exit( 1 )



outMessage = 'Hello WOrld'

print('sending ' + outMessage )
s.send( outMessage.encode() )

data = s.recv( 1024 ).decode()
print('Received ' + data )

print('sending ' + outMessage )
s.send( outMessage.encode() )

s.shutdown( socket.SHUT_WR )

while 1:
    data = s.recv( 1024 ).decode()
    print( 'received ' + data )
    if len(data) == 0:
        break
print( 'Zero length read. Closing' )
s.close()
    

                                                                              
