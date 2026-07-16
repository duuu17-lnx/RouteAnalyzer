from pathlib import Path
import os
import platform


class AppPaths:

    APP_NAME = "RouteAnalyzer"

    @classmethod
    def base_dir(cls):

        sistema = platform.system()

        #
        # Windows
        #

        if sistema == "Windows":

            base = os.getenv("APPDATA")

            if base:

                caminho = Path(base) / cls.APP_NAME

            else:

                caminho = Path.home() / cls.APP_NAME

        #
        # Linux
        #

        else:

            base = os.getenv("XDG_CONFIG_HOME")

            if base:

                caminho = Path(base) / cls.APP_NAME

            else:

                caminho = Path.home() / ".config" / cls.APP_NAME

        caminho.mkdir(

            parents=True,

            exist_ok=True

        )

        return caminho

    @classmethod
    def reports_dir(cls):

        caminho = cls.base_dir() / "reports"

        caminho.mkdir(

            parents=True,

            exist_ok=True

        )

        return caminho

    @classmethod
    def config_file(cls):

        return cls.base_dir() / "config.json"