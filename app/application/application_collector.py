from urllib.parse import urljoin

from app.application.application_http import ApplicationHTTP


class ApplicationCollector:

    MAX_REDIRECTS = 10

    def collect(

        self,

        url: str

    ):

        http = ApplicationHTTP()

        #
        # Primeira requisição
        #

        resultado = http.execute(

            url

        )

        visitadas = {

            resultado.url

        }

        atual = resultado

        redirects = 0

        #
        # Segue manualmente toda a cadeia
        #

        while (

            atual.redirect

            and

            atual.location

            and

            redirects < self.MAX_REDIRECTS

        ):

            #
            # Alguns servidores retornam Location relativo
            #

            proxima_url = urljoin(

                atual.url,

                atual.location

            )

            #
            # Evita loop infinito
            #

            if proxima_url in visitadas:

                break

            visitadas.add(

                proxima_url

            )

            novo = http.execute(

                proxima_url

            )

            #
            # Encadeia os resultados
            #

            atual.redirect_result = novo

            atual = novo

            redirects += 1

        return resultado