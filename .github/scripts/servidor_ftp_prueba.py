"""Servidor FTP de PRUEBA en 127.0.0.1 (pyftpdlib) para test_desplegar_ftp.sh. Nunca toca el servidor real.

    python servidor_ftp_prueba.py tls|plano PUERTO RAIZ USUARIO CLAVE LOG [CERT KEY]

tls: exige AUTH TLS antes del login y PROT P en los datos (como debe quedar el deploy).
plano: FTP sin TLS (el caso que el deploy tiene que RECHAZAR sin mandar el usuario).
"""
import logging
import sys

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler, TLS_FTPHandler
from pyftpdlib.servers import FTPServer

modo, puerto, raiz, usuario, clave, log = sys.argv[1:7]
autorizador = DummyAuthorizer()
autorizador.add_user(usuario, clave, raiz, perm="elradfmwMT")
if modo == "tls":
    manejador = TLS_FTPHandler
    manejador.certfile, manejador.keyfile = sys.argv[7], sys.argv[8]
    manejador.tls_control_required = True
    manejador.tls_data_required = True
else:
    manejador = FTPHandler
manejador.authorizer = autorizador
# Rangos pasivos que no se pisan entre servidores: 2121 -> 12100-12119, 2122 -> 12200-12219, ...
manejador.passive_ports = range((int(puerto) - 2000) * 100, (int(puerto) - 2000) * 100 + 20)
logging.basicConfig(filename=log, level=logging.DEBUG)
FTPServer(("127.0.0.1", int(puerto)), manejador).serve_forever()
