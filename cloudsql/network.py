import mysql.connector
import googleapiclient.discovery
from OpenSSL import crypto, SSL
import warnings
import sys
import socket

class MySQLSSLSocket(mysql.connector.network.BaseMySQLSocket):

    def __init__(self, ssl_context, ip_address):
        super(MySQLSSLSocket, self).__init__()
        
        self._ssl_context = ssl_context
        self._ip_address = ip_address

    def open_connection(self):
        self.sock = SSL.Connection(self._ssl_context, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        self.sock.settimeout(self._connection_timeout)
        self.sock.connect((self._ip_address, 3307))

