#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer


class EchoHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        self.wfile.write("Hemos recibido tu peticion")
        clientIP, clientPort = self.client_address
        print 'client IP: ' + clientIP + ':' + str(clientPort)
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read().strip()
            print "El cliente nos manda " + line
            if not line:
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer(("", 6001), EchoHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
