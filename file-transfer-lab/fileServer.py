#! /usr/bin/env python3

import sys,os
sys.path.append("../lib")       # for params
import re, socket, params

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)



from framedSock import framedSend, framedReceive


# do the multiple client
def client_fork():

    while True:
        sock, addr = lsock.accept()
        print("connection rec'd from", addr)
        data = sock.recv( 100 )
        if not data: # check if data is being recieved
            break # check if connection still exists
        while(data): # while data is being sent
            file_out.write(data)
            data = sock.recv(100)

        file_out.close()
        sock.send( b'Finished transfer' )
        sock.close()

i = 0 # keep track of file written
while True:
    rc = os.fork() # fork
    if rc < 0:
        print('error')
        sys.exit(1)
    elif rc == 0: # child
        file_out = open( 'out_' + str( i ) , 'wb' )
        i = i + 1
        client_fork() # write to file
    else:
        child = os.wait()


