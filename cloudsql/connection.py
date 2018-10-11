import mysql.connector
import googleapiclient.discovery
from OpenSSL import crypto, SSL
import warnings
import sys
import socket

from cachetools import cached

from .network import MySQLSSLSocket

warnings.filterwarnings("ignore", "Your application has authenticated using end user credentials")

class MySQLConnection(mysql.connector.MySQLConnection):
    
    def config(self, **kwargs):
        super(MySQLConnection, self).config(**kwargs)
        
        self._project, self._region, self._instance = self._host.split(':', 2)
        self._metadata = self._get_instance_metadata()
 
    def _get_connection(self, prtcls=None):
        context = self._get_instance_ssl_context()
        conn = MySQLSSLSocket(context, self._metadata['ipAddresses'][0]['ipAddress'])
        conn.set_connection_timeout(self._connection_timeout)
        
        return conn

    def _get_instance_metadata(self):
        request = self._api_client().instances().get(project = self._project, instance = self._instance)
        metadata = request.execute()

        if metadata['backendType'] != 'SECOND_GEN':
            raise Exception('Instance "%s" is not a 2nd generation MySQL instance.' % self._instance_name )

        if not metadata['ipAddresses']:
            raise Exception('Instance "%s" has no IP addresses.' % self._instance_name)
        
        return metadata

    def _get_instance_ssl_context(self):
        key = crypto.PKey()
        key.generate_key(crypto.TYPE_RSA, 2048)
        
        public_key = crypto.dump_publickey(crypto.FILETYPE_PEM, key)
        private_key = crypto.dump_privatekey(crypto.FILETYPE_PEM, key)

        request = self._api_client().sslCerts().createEphemeral(project=self._project,
                instance=self._instance,
                body={'public_key': public_key})

        ephemeral = request.execute()

        client_cert = crypto.load_certificate(crypto.FILETYPE_PEM, ephemeral['cert'])
        ca_cert = crypto.load_certificate(crypto.FILETYPE_PEM, self._metadata['serverCaCert']['cert'])

        context = SSL.Context(SSL.TLSv1_2_METHOD)
        context.set_verify(SSL.VERIFY_PEER, self._verify_cert)
        context.use_privatekey(key)
        context.use_certificate(client_cert)
        context.get_cert_store().add_cert(ca_cert)

        return context

    def _verify_cert(self, conn, cert, errnum, depth, ok):
        certsubject = crypto.X509Name(cert.get_subject())
        commonname = certsubject.commonName
        
        return ok

    def _api_client(self):
        return googleapiclient.discovery.build('sqladmin', 'v1beta4')
