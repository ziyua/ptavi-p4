#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import os
import time


class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """
    LOG_NAME = 'registered.txt'
    Users = {}

    def handle(self):
        """
        1. Imprima IP:port de client
        2. Recibir
        "REGISTER sip:luke@polismassa.com SIP/2.0\r\nExpires: 3600\r\n\r\n"
        3. Si message correcta ->
            User = luke@polismassa.com; Expires = 3600
        4. Expires no es igual a 0 -> add diccionario 'Users';
                             si es -> del diccionario 'Users';
                                    si no exist en dic 'Pass';
                       Luego envia -> SIP/2.0 200 OK\r\n\r\n ;
                                escribir en 'registered.txt' ;
        """
        # Escribe dirección y puerto del cliente (de tupla client_address)
        clientIP, clientPort = self.client_address
        print 'client IP: ' + clientIP + ':' + str(clientPort)
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read().strip()
            if line[:8] == 'REGISTER' and line.split()[-2] == 'Expires:':
                #User and time expired
                User = line.split()[1].lstrip('sip:')
                Expires = int(line.split()[-1])
                if Expires != 0:
                    self.Users[User] = self.client_address
                elif User in self.Users:
                    del self.Users[User]
                self.wfile.write('SIP/2.0 200 OK\r\n\r\n')
                self.register2file(User, clientIP)
                print "Users is: ", self.Users
            if not line:
                break

    def register2file(self, User, IP):
        """
            si exist 'registered.txt' añade info.
            no exist añade 'User \t IP \t Expires \r\n'
                     añade info.
        """
        if os.path.exists(self.LOG_NAME):
            log_file = open(self.LOG_NAME, 'a')
        else:
            log_file = open(self.LOG_NAME, 'w')
            log_file.write('User \t IP \t Expires \r\n')
        now = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))
        log_file.write(User + ' \t ' + IP + ' \t ' + now + '\r\n')
        log_file.close()


if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer(("", 6001), SIPRegisterHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
