class PerformanceAnalyzer:

    def analyze(

        self,

        resultado

    ):

        #
        # Analisa sempre o resultado efetivo da requisição
        #

        resultado = resultado.get_final()

        etapas = {

            "DNS": resultado.dns_time,

            "TCP": resultado.tcp_time,

            "TLS": resultado.tls_time,

            "Aplicação": resultado.application_time,

            "Transferência": resultado.transfer_time

        }

        #
        # Remove etapas sem tempo
        #

        etapas = {

            nome: tempo

            for nome, tempo in etapas.items()

            if tempo > 0

        }

        if not etapas:

            return None

        #
        # Etapa que mais consumiu tempo
        #

        etapa = max(

            etapas,

            key=etapas.get

        )

        tempo = etapas[etapa]

        total = resultado.total_time

        percentual = 0.0

        if total > 0:

            percentual = round(

                (tempo / total) * 100,

                1

            )

        #
        # Ranking das etapas
        #

        ranking = sorted(

            etapas.items(),

            key=lambda item: item[1],

            reverse=True

        )

        return {

            "etapa": etapa,

            "tempo": tempo,

            "percentual": percentual,

            "ranking": ranking

        }