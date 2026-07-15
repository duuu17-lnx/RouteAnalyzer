import re
import subprocess
import time

from app.dns.dns_result import DNSResult


class WindowsDNSCollector:

    def query(self, dominio, dns):

        resultado = DNSResult()

        resultado.origem = dns["origem"]
        resultado.nome = dns["nome"]

        if dns["ip"] is None:

            resultado.servidor = "Sistema"

            comando = [

                "nslookup",

                dominio

            ]

        else:

            resultado.servidor = dns["ip"]

            comando = [

                "nslookup",

                dominio,

                dns["ip"]

            ]

        inicio = time.perf_counter()

        try:

            processo = subprocess.run(

                comando,

                capture_output=True,

                text=True,

                encoding="cp850",

                errors="ignore",

                timeout=5

            )

            resultado.tempo = round(

                (time.perf_counter() - inicio) * 1000,

                2

            )

            saida = processo.stdout
            saida_upper = saida.upper()

            #
            # NXDOMAIN
            #

            if (

                "NON-EXISTENT DOMAIN" in saida_upper

                or

                "NXDOMAIN" in saida_upper

            ):

                resultado.status = "NXDOMAIN"

                resultado.erro = "O domínio informado não existe."

                return resultado

            #
            # SERVFAIL
            #

            if "SERVFAIL" in saida_upper:

                resultado.status = "SERVFAIL"

                resultado.erro = "O servidor DNS retornou SERVFAIL."

                return resultado

            #
            # REFUSED
            #

            if "REFUSED" in saida_upper:

                resultado.status = "REFUSED"

                resultado.erro = "O servidor DNS recusou a consulta."

                return resultado

            #
            # Timeout
            #

            if (

                "TIMED OUT" in saida_upper

                or

                "TIMEOUT" in saida_upper

            ):

                resultado.status = "Timeout"

                resultado.erro = "O servidor DNS não respondeu."

                return resultado

            #
            # Sem resposta
            #

            if (

                "NO RESPONSE" in saida_upper

                or

                "NO SERVERS COULD BE REACHED" in saida_upper

            ):

                resultado.status = "Erro"

                resultado.erro = "Nenhum servidor DNS respondeu."

                return resultado

            #
            # Procura IPv4
            #

            ipv4 = re.findall(

                r"\b(?:\d{1,3}\.){3}\d{1,3}\b",

                saida

            )

            if dns["ip"]:

                ipv4 = [

                    ip

                    for ip in ipv4

                    if ip != dns["ip"]

                ]

            if ipv4:

                resultado.resposta = ipv4[-1]

                resultado.status = "OK"

                return resultado

            #
            # Erro desconhecido
            #

            resultado.status = "Erro"

            resultado.erro = saida.strip()

            return resultado

        except subprocess.TimeoutExpired:

            resultado.status = "Timeout"

            resultado.erro = "Tempo limite excedido."

            return resultado

        except FileNotFoundError:

            resultado.status = "Erro"

            resultado.erro = "Comando nslookup não encontrado."

            return resultado

        except Exception as e:

            resultado.status = "Erro"

            resultado.erro = str(e)

            return resultado