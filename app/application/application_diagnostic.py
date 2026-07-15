from urllib.parse import urlparse

from app.application.application_dns import ApplicationDNS
from app.application.application_runner import ApplicationRunner
from app.application.application_statistics import ApplicationStatistics
from app.application.application_analyzer import ApplicationAnalyzer
from app.application.application_table import ApplicationTable


class ApplicationDiagnostic:

    def execute(self):

        print()

        print("=" * 92)
        print("Diagnóstico de Aplicação".center(92))
        print("=" * 92)
        print()

        print("Informe o domínio ou URL da aplicação:")
        print()

        url = input("> ").strip()

        if not url:

            print()
            print("Destino inválido.")
            input("\nPressione ENTER para retornar...")
            return None

        #
        # Escolha do resolvedor DNS
        #

        print()

        print("Resolvedor DNS")
        print()

        print("[1] Utilizar o DNS padrão (201.159.154.3)")
        print("[2] Informar outro resolvedor")
        print()

        opcao = input("Opção: ").strip()

        if opcao == "2":

            print()

            servidor_dns = input(

                "Informe o endereço IPv4 do resolvedor DNS: "

            ).strip()

            if not servidor_dns:

                print()

                print("Resolvedor inválido.")

                input("\nPressione ENTER para retornar...")

                return None

        else:

            servidor_dns = "201.159.154.3"

        #
        # Extrai apenas o HOST para consulta DNS,
        # preservando exatamente a URL informada
        # para os testes HTTP.
        #

        if "://" not in url:

            url_http = "https://" + url

        else:

            url_http = url

        dominio = urlparse(url_http).hostname

        if not dominio:

            print()

            print("Não foi possível identificar o domínio informado.")

            input("\nPressione ENTER para retornar...")

            return None

        #
        # Consulta DNS
        #

        print()

        print(f"Consultando DNS ({servidor_dns})...")

        dns = ApplicationDNS().resolve(

            dominio,

            servidor_dns

        )

        if dns.status != "OK":

            print()

            print("=" * 92)
            print("Falha na resolução DNS".center(92))
            print("=" * 92)
            print()

            print(f"Resolvedor......: {dns.servidor}")
            print(f"Status..........: {dns.status}")

            if dns.erro:

                print(f"Erro............: {dns.erro}")

            print()

            print("Conclusão")
            print("-" * 92)

            if dns.status == "NXDOMAIN":

                print("• O domínio informado não existe.")

            elif dns.status == "SERVFAIL":

                print("• O resolvedor DNS retornou SERVFAIL.")

            elif dns.status == "REFUSED":

                print("• O resolvedor DNS recusou a consulta.")

            elif dns.status == "Timeout":

                print("• O resolvedor DNS não respondeu dentro do tempo esperado.")

            else:

                print(f"• Falha durante a resolução DNS ({dns.status}).")

            input("\nPressione ENTER para retornar ao menu...")

            return None

        print()

        print("DNS resolvido com sucesso.")
        print(f"Resolvedor.......: {dns.servidor}")
        print(f"Endereço IPv4....: {dns.resposta}")
        print(f"Tempo............: {dns.tempo:.2f} ms")
        print()

        print("Executando diagnóstico...\n")

        #
        # Executa exatamente a URL informada pelo usuário
        #

        resultados = ApplicationRunner().run(

            url,

            execucoes=5

        )

        if not resultados:

            print("Nenhuma resposta obtida.")

            input("\nPressione ENTER para retornar...")

            return None

        #
        # Estatísticas
        #

        estatisticas = ApplicationStatistics().calculate(

            resultados

        )

        #
        # Última execução válida
        #

        resultado = None

        for item in reversed(resultados):

            if item.sucesso:

                resultado = item

                break

        if resultado is None:

            resultado = resultados[-1]

        #
        # Análise
        #

        responsabilidade, conclusoes = ApplicationAnalyzer().analyze(

            resultado,

            estatisticas

        )

        #
        # Exibição
        #

        ApplicationTable().show(

            resultado,

            responsabilidade,

            conclusoes,

            estatisticas

        )

        input(

            "Pressione ENTER para retornar ao menu..."

        )

        #
        # Retorna a análise para utilização
        # pelo exportador da sessão.
        #

        return {

            "tipo": "application",

            "resultado": resultado,

            "responsabilidade": responsabilidade,

            "conclusoes": conclusoes,

            "estatisticas": estatisticas

        }