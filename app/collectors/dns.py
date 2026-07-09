import ipaddress
import socket


class DNSCollector:

    def resolve(self, destino: str):

        try:

            ipaddress.ip_address(destino)

            return destino

        except ValueError:

            pass

        try:

            return socket.gethostbyname(destino)

        except socket.gaierror:

            return None

    def reverse(self, ip: str):

        try:

            return socket.gethostbyaddr(ip)[0]

        except Exception:

            return ip