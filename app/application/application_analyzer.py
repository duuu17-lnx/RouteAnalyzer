from app.application.performance_analyzer import PerformanceAnalyzer


class ApplicationAnalyzer:

    def analyze(

        self,

        resultado,

        estatisticas

    ):

        conclusoes = []

        responsabilidade = {

            "DNS": "OK",

            "Rede": "OK",

            "TLS": "OK",

            "Aplicação": "OK",

            "Consistência": "OK"

        }

        #
        # Nenhuma execução HTTP válida
        #

        if estatisticas["validas"] == 0:

            responsabilidade["Rede"] = "Não testada"

            responsabilidade["TLS"] = "Não testado"

            responsabilidade["Aplicação"] = "Não testada"

            responsabilidade["Consistência"] = "Não aplicável"

            if resultado.erro == "DNS":

                responsabilidade["DNS"] = "Falha"

                conclusoes.append(

                    "Não foi possível resolver o domínio informado."

                )

            elif resultado.erro == "TCP":

                responsabilidade["Rede"] = "Falha"

                conclusoes.append(

                    "Não foi possível estabelecer conexão TCP com o servidor."

                )

            elif resultado.erro == "TLS":

                responsabilidade["TLS"] = "Falha"

                conclusoes.append(

                    "Não foi possível estabelecer uma conexão TLS."

                )

            elif resultado.erro == "Timeout":

                responsabilidade["Rede"] = "Timeout"

                conclusoes.append(

                    "A conexão expirou antes da conclusão da requisição."

                )

            else:

                conclusoes.append(

                    "Nenhuma requisição HTTP pôde ser concluída."

                )

            return responsabilidade, conclusoes

        #
        # Consistência
        #

        if estatisticas["intermitencia"]:

            responsabilidade["Consistência"] = "Intermitente"

            conclusoes.append(

                "Foi observado comportamento intermitente entre as execuções."

            )

        else:

            conclusoes.append(

                "Todas as execuções apresentaram comportamento consistente."

            )

        #
        # Distribuição HTTP
        #

        http = estatisticas["http"]

        if len(http) == 1:

            codigo = next(iter(http))

            quantidade = http[codigo]

            conclusoes.append(

                f"Todas as {quantidade} execuções retornaram HTTP {codigo}."

            )

        else:

            distribuicao = ", ".join(

                f"HTTP {codigo}: {quantidade}"

                for codigo, quantidade in sorted(http.items())

            )

            conclusoes.append(

                f"Foram observadas respostas distintas durante os testes ({distribuicao})."

            )

        #
        # Redirect
        #

        if resultado.redirect:

            responsabilidade["Aplicação"] = "Redirect"

        #
        # Classificação da aplicação
        #

        else:

            codigo = resultado.http_code

            if codigo == 403:

                responsabilidade["Aplicação"] = "Restrição"

            elif codigo == 404:

                responsabilidade["Aplicação"] = "Recurso"

            elif codigo in (500, 502):

                responsabilidade["Aplicação"] = "Erro"

            elif codigo == 503:

                responsabilidade["Aplicação"] = "Indisponível"

            elif codigo >= 400:

                responsabilidade["Aplicação"] = f"HTTP {codigo}"

        #
        # Desempenho
        #

        performance = PerformanceAnalyzer().analyze(

            resultado

        )

        if performance:

            etapa = performance["etapa"]

            percentual = performance["percentual"]

            tempo = performance["tempo"]

            if percentual >= 60:

                conclusoes.append(

                    f"A etapa que mais consumiu tempo foi {etapa.lower()} ({tempo:.2f} ms), representando aproximadamente {percentual:.1f}% do tempo total."

                )

        #
        # Redirect
        #

        if resultado.redirect:

            conclusoes.append(

                f"O servidor realizou {resultado.redirects} redirecionamento(s) HTTP."

            )

        return responsabilidade, conclusoes