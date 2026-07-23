import ipaddress
import re
import socket


class DNSCollector:

    def resolve(self, destino: str):

        destino = destino.strip()

        #
        # IPv4 válido
        #

        try:

            ipaddress.ip_address(destino)

            return destino

        except ValueError:

            pass

        #
        # Domínio válido
        #

        if not re.fullmatch(

            r"^(?=.{1,253}$)(?!-)(?:[A-Za-z0-9-]{1,63}\.)+[A-Za-z]{2,63}$",

            destino

        ):

            return None

        try:

            return socket.gethostbyname(destino)

        except socket.gaierror:

            return None

    def reverse(self, ip: str):

        try:

            return socket.gethostbyaddr(ip)[0]

        except Exception:

            return ip