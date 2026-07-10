import platform

from app.collectors.mtr import MTRCollector
from app.collectors.windows_mtr import WindowsMTRCollector


class CollectorFactory:

    def get(self):

        if platform.system() == "Windows":

            return WindowsMTRCollector()

        return MTRCollector()