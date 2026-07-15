from app.application.application_collector import ApplicationCollector


class ApplicationRunner:

    def run(

        self,

        url,

        execucoes=5

    ):

        collector = ApplicationCollector()

        resultados = []

        for numero in range(1, execucoes + 1):

            resultado = collector.collect(

                url

            )

            resultado.execucao = numero

            resultados.append(

                resultado

            )

        return resultados