import re
import statistics
import subprocess


class WindowsPing:

    def run(

        self,

        host: str,

        pacotes: int = 80

    ):

        comando = [

            "ping",

            "-n",

            str(pacotes),

            "-w",

            "1000",

            host

        ]

        processo = subprocess.run(

            comando,

            capture_output=True,

            text=True,

            encoding="cp850",

            errors="ignore"

        )

        saida = processo.stdout

        enviados = pacotes

        recebidos = 0

        tempos = []

        ultimo = 0.0

        #
        # Extrai todos os tempos das respostas
        #

        for linha in saida.splitlines():

            match = re.search(

                r"tempo[=<]\s*(\d+)\s*ms",

                linha,

                re.IGNORECASE

            )

            if not match:

                match = re.search(

                    r"time[=<]\s*(\d+)\s*ms",

                    linha,

                    re.IGNORECASE

                )

            if match:

                valor = float(

                    match.group(1)

                )

                tempos.append(

                    valor

                )

                ultimo = valor

                recebidos += 1

        #
        # Perda de pacotes
        #

        loss = 100.0

        #
        # Windows em português:
        # Pacotes: Enviados = X, Recebidos = Y, Perdidos = Z (0% de perda)
        #

        match = re.search(

            r"Perdidos\s*=\s*\d+\s*\((\d+)%",

            saida,

            flags=re.IGNORECASE

        )

        #
        # Windows em inglês:
        # Lost = Z (0% loss)
        #

        if not match:

            match = re.search(

                r"Lost\s*=\s*\d+\s*\((\d+)%",

                saida,

                flags=re.IGNORECASE

            )

        if match:

            loss = float(match.group(1))

        #
        # Nenhuma resposta
        #

        if not tempos:

            print(f"[PING] {host} | SEM RESPOSTA")

            return {

                "loss": loss,

                "sent": enviados,

                "received": recebidos,

                "last": 0.0,

                "avg": 0.0,

                "best": 0.0,

                "worst": 0.0,

                "stdev": 0.0

            }

        #
        # Estatísticas
        #

        best = min(

            tempos

        )

        worst = max(

            tempos

        )

        avg = round(

            sum(tempos) / len(tempos),

            2

        )

        if len(tempos) > 1:

            stdev = round(

                statistics.pstdev(

                    tempos

                ),

                2

            )

        else:

            stdev = 0.0


        return {

            "loss": loss,

            "sent": enviados,

            "received": recebidos,

            "last": ultimo,

            "avg": avg,

            "best": best,

            "worst": worst,

            "stdev": stdev

        }