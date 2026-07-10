import re
import subprocess


class WindowsTracert:

    def run(self, destino):

        comando = [

            "tracert",

            "-d",

            destino

        ]

        resultado = subprocess.run(

            comando,

            capture_output=True,

            text=True,

            encoding="cp850",

            errors="ignore"

        )

        if resultado.returncode != 0:

            raise RuntimeError(resultado.stderr)

        hops = []

        for linha in resultado.stdout.splitlines():

            linha = linha.strip()

            #
            # Apenas linhas iniciadas pelo número do hop
            #

            if not re.match(r"^\d+", linha):

                continue

            #
            # Extrai o número do hop
            #

            numero = int(

                re.match(

                    r"^(\d+)",

                    linha

                ).group(1)

            )

            #
            # Extrai o IP
            #

            ips = re.findall(

                r"(?:\d{1,3}\.){3}\d{1,3}",

                linha

            )

            if not ips:

                continue

            ip = ips[-1]

            #
            # Extrai os três tempos
            #

            tempos = []

            for tempo in re.findall(

                r"(<\d+|\d+)\s*ms",

                linha,

                flags=re.IGNORECASE

            ):

                if tempo.startswith("<"):

                    tempos.append(0.5)

                else:

                    tempos.append(float(tempo))

            #
            # Perda baseada no tracert
            #

            perdas = linha.count("*")

            loss = round(

                perdas / 3 * 100,

                1

            )

            #
            # Se todos foram perdidos
            #

            if not tempos:

                avg = 0.0
                best = 0.0
                worst = 0.0

            else:

                avg = round(

                    sum(tempos) / len(tempos),

                    2

                )

                best = min(tempos)

                worst = max(tempos)

            hops.append(

                {

                    "numero": numero,

                    "ip": ip,

                    "loss": loss,

                    "avg": avg,

                    "best": best,

                    "worst": worst

                }

            )

        return hops