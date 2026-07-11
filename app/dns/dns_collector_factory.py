import platform

from app.dns.dns_collector import DNSCollector
from app.dns.windows_dns_collector import WindowsDNSCollector


class DNSCollectorFactory:

    def get(self):

        if platform.system() == "Windows":

            return WindowsDNSCollector()

        return DNSCollector()