import re
import subprocess
import time

from app.dns.dns_result import DNSResult


class DNSCollector:

    def query(self, dominio, dns):

        resultado = DNSResult()

        resultado.origem = dns["origem"]
        resultado.nome = dns["nome"]

        #
        # Monta comando
        #

        if dns["ip"] is None:

            resultado.servidor = "Sistema"

            comando = [
                "dig",
                dominio,
                "A",
                "+time=2",
                "+tries=1"
            ]

        else:

            resultado.servidor = dns["ip"]

            comando = [
                "dig",
                f"@{dns['ip']}",
                dominio,
                "A",
                "+time=2",
                "+tries=1"
            ]

        inicio = time.perf_counter()

        try:

            processo = subprocess.run(

                comando,

                capture_output=True,

                text=True,

                timeout=3

            )

            resultado.tempo = round(

                (time.perf_counter() - inicio) * 1000,

                2

            )

            saida = processo.stdout

            #
            # Status DNS
            #

            status = re.search(

                r"status:\s*([A-Z]+)",

                saida

            )

            if status:

                status = status.group(1)

            else:

                status = "UNKNOWN"

            #
            # Extrai IPv4
            #

            ipv4 = re.findall(

                r"\b(?:\d{1,3}\.){3}\d{1,3}\b",

                saida

            )

            if ipv4:

                resultado.resposta = ipv4[0]

            #
            # Classificação
            #

            if status == "NOERROR":

                resultado.status = "OK"

            elif status == "NXDOMAIN":

                resultado.status = "NXDOMAIN"

            elif status == "SERVFAIL":

                resultado.status = "SERVFAIL"

            elif status == "REFUSED":

                resultado.status = "REFUSED"

            else:

                resultado.status = status

            return resultado

        except subprocess.TimeoutExpired:

            resultado.status = "Timeout"

            return resultado

        except FileNotFoundError:

            resultado.status = "Erro"

            resultado.erro = "Comando dig não encontrado."

            return resultado

        except Exception as e:

            resultado.status = "Erro"

            resultado.erro = str(e)

            return resultado