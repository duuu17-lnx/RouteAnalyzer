import re
import subprocess


class WindowsTracert:

    def run(

        self,

        destino

    ):

        comando = [

            "tracert",

            "-d",

            "-w",

            "1000",

            destino

        ]

        processo = subprocess.Popen(

            comando,

            stdout=subprocess.PIPE,

            stderr=subprocess.PIPE,

            text=True,

            encoding="cp850",

            errors="ignore"

        )

        hops = []

        try:

            while True:

                linha = processo.stdout.readline()

                if not linha:

                    break

                hop = self._parse_hop(

                    linha

                )

                if hop is None:

                    continue

                hops.append(

                    hop

                )

                if hop["ip"] == destino:

                    processo.terminate()

                    break

        finally:

            try:

                processo.wait(

                    timeout=2

                )

            except subprocess.TimeoutExpired:

                processo.kill()

        if not hops:

            raise RuntimeError(

                "Não foi possível descobrir a rota."

            )

        return hops


    def _parse_hop(

        self,

        linha

    ):

        linha = linha.strip()

        if not linha:

            return None

        if not re.match(

            r"^\d+",

            linha

        ):

            return None

        numero = int(

            re.match(

                r"^(\d+)",

                linha

            ).group(1)

        )

        ips = re.findall(

            r"(?:\d{1,3}\.){3}\d{1,3}",

            linha

        )

        #
        # Hop sem resposta
        #

        if not ips:

            return {

                "numero": numero,

                "ip": None,

                "loss": 100.0,

                "avg": 0.0,

                "best": 0.0,

                "worst": 0.0

            }

        ip = ips[-1]

        #
        # Tempos retornados pelo tracert
        #

        tempos = []

        for tempo in re.findall(

            r"(<\d+|\d+)\s*ms",

            linha,

            flags=re.IGNORECASE

        ):

            if tempo.startswith("<"):

                tempos.append(

                    0.5

                )

            else:

                tempos.append(

                    float(

                        tempo

                    )

                )

        #
        # Perda observada pelo tracert
        #

        perdas = linha.count("*")

        loss = round(

            perdas / 3 * 100,

            1

        )

        #
        # Estatísticas do RTT do tracert
        #

        if tempos:

            avg = round(

                sum(tempos) / len(tempos),

                2

            )

            best = min(

                tempos

            )

            worst = max(

                tempos

            )

        else:

            avg = 0.0

            best = 0.0

            worst = 0.0

        return {

            "numero": numero,

            "ip": ip,

            "loss": loss,

            "avg": avg,

            "best": best,

            "worst": worst

        }