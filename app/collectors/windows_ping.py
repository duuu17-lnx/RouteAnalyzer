import re
import statistics
import subprocess


class WindowsPing:

    def run(self, host: str, pacotes: int = 80):

        comando = [

            "ping",

            "-n",

            str(pacotes),

            host

        ]

        resultado = subprocess.run(

            comando,

            capture_output=True,

            text=True,

            encoding="cp850",

            errors="ignore"

        )

        if resultado.returncode != 0:

            return {

                "loss": 100.0,

                "sent": pacotes,

                "received": 0,

                "last": 0.0,

                "avg": 0.0,

                "best": 0.0,

                "worst": 0.0,

                "stdev": 0.0

            }

        saida = resultado.stdout

        #
        # Todos os tempos individuais
        #

        tempos = []

        for tempo in re.findall(

            r"tempo[=<]\s*(\d+)ms",

            saida,

            flags=re.IGNORECASE

        ):

            tempos.append(float(tempo))

        #
        # Perda
        #

        perda = 100.0

        match = re.search(

            r"Perdidos = \d+ \((\d+)%",

            saida,

            flags=re.IGNORECASE

        )

        if match:

            perda = float(match.group(1))

        #
        # Sem respostas
        #

        if not tempos:

            return {

                "loss": perda,

                "sent": pacotes,

                "received": 0,

                "last": 0.0,

                "avg": 0.0,

                "best": 0.0,

                "worst": 0.0,

                "stdev": 0.0

            }

        #
        # Estatísticas
        #

        media = round(

            statistics.mean(tempos),

            2

        )

        minimo = round(

            min(tempos),

            2

        )

        maximo = round(

            max(tempos),

            2

        )

        ultimo = round(

            tempos[-1],

            2

        )

        if len(tempos) > 1:

            desvio = round(

                statistics.stdev(tempos),

                2

            )

        else:

            desvio = 0.0

        return {

            "loss": perda,

            "sent": pacotes,

            "received": len(tempos),

            "last": ultimo,

            "avg": media,

            "best": minimo,

            "worst": maximo,

            "stdev": desvio

        }