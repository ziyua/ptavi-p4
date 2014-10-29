#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Cliente UDP simple.
"""
client envia
Protocol SIP:
    REGISTER sip:name@email.com SIP/2.0\r\n
    Expires: 3600\r\n
    \r\n
Receibe:
    SIP/2.0 200 OK\r\n
    \r\n
"""

if len(sys.argv) != 6:
    sys.exit('Usage: client.py ip puerto register sip_address expires_value')

# Dirección IP del servidor.
SERVER = sys.argv[1]
#  Por si se introduce un parámetro no numérico en "PORT"
PORT = int(sys.argv[2])
# Contenido que vamos a enviar
# Por si acaso el usuario introduce otro método que no sea 'register'
if sys.argv[3] == 'register':
    LINE = sys.argv[3].upper() + ' sip:' + sys.argv[4] + ' ' + 'SIP/2.0\r\n'
    EXPIRES = 'Expires:' + ' ' + sys.argv[5] + '\r\n'
else:
    sys.exit('Usage: client.py ip puerto register sip_address expires_value')

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))

print "Enviando: " + LINE
my_socket.send(LINE + EXPIRES + '\r\n')
data = my_socket.recv(1024)

print 'Recibido -- ', data
print "Terminando socket..."

# Cerramos todo
my_socket.close()
print "Fin."
