import re
import subprocess
import time

from app.dns.dns_result import DNSResult


class WindowsDNSCollector:

    def query(self, dominio, dns):

        resultado = DNSResult()

        resultado.origem = dns["origem"]
        resultado.nome = dns["nome"]

        #
        # Resolve usando o DNS configurado no sistema
        #

        if dns["ip"] is None:

            resultado.servidor = "Sistema"

            comando = [
                "nslookup",
                dominio
            ]

        #
        # Resolve usando um DNS específico
        #

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
            #
            # Verifica erros
            #

            saida_upper = saida.upper()

            if (

                "NON-EXISTENT DOMAIN" in saida_upper

                or

                "***" in saida_upper

                or

                "NXDOMAIN" in saida_upper

            ):

                resultado.status = "NXDOMAIN"

                return resultado

            #
            # Procura o último IPv4 retornado
            #

            ipv4 = re.findall(

                r"\b(?:\d{1,3}\.){3}\d{1,3}\b",

                saida

            )

            #
            # Remove o IP do servidor DNS utilizado
            #

            if dns["ip"]:

                ipv4 = [

                    ip

                    for ip in ipv4

                    if ip != dns["ip"]

                ]

            #
            # Se encontrou resposta
            #

            if ipv4:

                resultado.resposta = ipv4[-1]

                resultado.status = "OK"

            else:

                resultado.status = "Erro"

            return resultado
        except subprocess.TimeoutExpired:

            resultado.status = "Timeout"

            return resultado

        except FileNotFoundError:

            resultado.status = "Erro"

            resultado.erro = "Comando nslookup não encontrado."

            return resultado

        except Exception as e:

            resultado.status = "Erro"

            resultado.erro = str(e)

            return resultado