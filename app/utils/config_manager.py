from app.models.analysis_config import AnalysisConfig
from app.utils.app_paths import AppPaths


class ConfigManager:

    def __init__(self):

        self.file = AppPaths.config_file()

    def save(self, config):

        with open(

            self.file,

            "w",

            encoding="utf-8"

        ) as f:

            f.write(f"{config.execucoes}\n")
            f.write(f"{config.ciclos}\n")

    def load(self):

        if not self.file.exists():

            return None

        try:

            with open(

                self.file,

                "r",

                encoding="utf-8"

            ) as f:

                linhas = [

                    x.strip()

                    for x in f.readlines()

                ]

            execucoes = int(linhas[0])

            ciclos = int(linhas[1])

            config = AnalysisConfig()

            config.execucoes = execucoes

            config.ciclos = ciclos

            #
            # Descobre automaticamente o perfil
            #

            if (

                execucoes == 2

                and

                ciclos == 30

            ):

                config.perfil = "Rápida"

            elif (

                execucoes == 3

                and

                ciclos == 80

            ):

                config.perfil = "Padrão"

            elif (

                execucoes == 5

                and

                ciclos == 300

            ):

                config.perfil = "Avançada"

            else:

                config.perfil = "Personalizada"

            return config

        except Exception:

            return None

    def ask(self, config):

        print()

        print("=" * 92)
        print("Última configuração utilizada".center(92))
        print("=" * 92)
        print()

        print(f"Perfil................: {config.perfil}")
        print(f"Execuções............: {config.execucoes}")
        print(f"Ciclos por execução..: {config.ciclos}")
        print(
            f"Amostras por hop.....: "
            f"{config.execucoes * config.ciclos}"
        )

        print()

        while True:

            resposta = input(

                "Utilizar esta configuração? [ENTER = Sim / N = Não]: "

            ).strip().lower()

            if resposta in ("", "s", "sim"):

                return True

            if resposta in ("n", "nao", "não"):

                return False

            print("Resposta inválida.")