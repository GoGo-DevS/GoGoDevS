"""Certificados de PRUEBA para test_desplegar_ftp.sh (nada de esto se usa contra el servidor real).

    python certs_prueba.py CARPETA

Deja en CARPETA: ca.pem (CA de prueba), srv.pem/srv.key (localhost, vigente, firmado por ca.pem),
vencido.pem/vencido.key (localhost, firmado por ca.pem, VENCIDO ayer) y otra-ca.pem (CA que no firmo nada).
"""
import datetime
import sys
from pathlib import Path

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.x509.oid import NameOID

dest = Path(sys.argv[1])
ahora = datetime.datetime.now(datetime.timezone.utc)


def clave():
    return ec.generate_private_key(ec.SECP256R1())


def guardar(nombre, cert, key=None):
    (dest / f"{nombre}.pem").write_bytes(cert.public_bytes(serialization.Encoding.PEM))
    if key is not None:
        (dest / f"{nombre}.key").write_bytes(key.private_bytes(
            serialization.Encoding.PEM, serialization.PrivateFormat.TraditionalOpenSSL, serialization.NoEncryption()))


def ca(nombre_cn):
    k = clave()
    n = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, nombre_cn)])
    c = (x509.CertificateBuilder().subject_name(n).issuer_name(n).public_key(k.public_key())
         .serial_number(x509.random_serial_number())
         .not_valid_before(ahora - datetime.timedelta(days=1)).not_valid_after(ahora + datetime.timedelta(days=2))
         .add_extension(x509.BasicConstraints(ca=True, path_length=0), critical=True)
         .add_extension(x509.KeyUsage(digital_signature=False, content_commitment=False, key_encipherment=False,
                                      data_encipherment=False, key_agreement=False, key_cert_sign=True,
                                      crl_sign=True, encipher_only=False, decipher_only=False), critical=True)
         .add_extension(x509.SubjectKeyIdentifier.from_public_key(k.public_key()), critical=False)
         .sign(k, hashes.SHA256()))
    return c, k


def servidor(ca_cert, ca_key, desde, hasta):
    k = clave()
    c = (x509.CertificateBuilder()
         .subject_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "localhost")]))
         .issuer_name(ca_cert.subject).public_key(k.public_key()).serial_number(x509.random_serial_number())
         .not_valid_before(desde).not_valid_after(hasta)
         .add_extension(x509.SubjectAlternativeName([x509.DNSName("localhost")]), critical=False)
         .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
         .add_extension(x509.ExtendedKeyUsage([x509.oid.ExtendedKeyUsageOID.SERVER_AUTH]), critical=False)
         .add_extension(x509.SubjectKeyIdentifier.from_public_key(k.public_key()), critical=False)
         .add_extension(x509.AuthorityKeyIdentifier.from_issuer_public_key(ca_key.public_key()), critical=False)
         .sign(ca_key, hashes.SHA256()))
    return c, k


ca_cert, ca_key = ca("CA de prueba")
guardar("ca", ca_cert)
guardar("srv", *servidor(ca_cert, ca_key, ahora - datetime.timedelta(hours=1), ahora + datetime.timedelta(days=1)))
guardar("vencido", *servidor(ca_cert, ca_key, ahora - datetime.timedelta(days=3), ahora - datetime.timedelta(days=1)))
guardar("otra-ca", ca("Otra CA")[0])
print("certificados de prueba en", dest)
