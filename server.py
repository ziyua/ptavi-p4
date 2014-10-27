#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import time


class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """
    LOG_NAME = 'registered.txt'
    Users = {}

    def handle(self):
        """
        Receive message and processa.
        """
        # Escribe dirección y puerto del cliente (de tupla client_address)
        clientIP, clientPort = self.client_address
        print 'client IP: ' + clientIP + ':' + str(clientPort)
        # Find user expired and Delete.
        for user in self.Users.keys():
            if time.time() > self.Users[user]['Expires']:
                del self.Users[user]
        # Leer informacion recibida.
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read().strip()
            if line[:8] == 'REGISTER' and line.split()[-2] == 'Expires:':
                # User and time expired
                User = line.split()[1][4:]
                Expires = int(line.split()[-1])
                # processa
                if Expires != 0:
                    # Añade user in diccionario Users.
                    self.Users[User] = {}
                    self.Users[User]['IP'] = self.client_address
                    self.Users[User]['Expires'] = time.time() + Expires
                elif User in self.Users:
                    # si user en tabla Users, borra. si no, pass.
                    del self.Users[User]
                # send message.
                self.wfile.write('SIP/2.0 200 OK\r\n\r\n')
                self.register2file()
                print "Users is: ", self.Users
            if not line:
                break

    def register2file(self):
        """
        register users in file
        """
        log_file = open(self.LOG_NAME, 'w')
        log_file.write('User \t IP \t Expires \r\n')
        for user in self.Users:
            log_file.write(user + ' \t ' +
                           self.Users[user]['IP'][0] + ' \t ' +
                           time.strftime('%Y-%m-%d %H:%M:%S',
                                         time.gmtime(self.Users[user]['Expires'])) +
                           '\r\n')
        log_file.close()


if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer(("", 6001), SIPRegisterHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
