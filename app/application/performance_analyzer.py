class PerformanceAnalyzer:

    DESCRICOES = {

        "DNS": (

            "resolução DNS",

            "antes de chegar ao servidor"

        ),

        "TCP": (

            "estabelecimento da conexão TCP",

            "antes de chegar ao servidor"

        ),

        "TLS": (

            "negociação TLS",

            "antes de chegar ao servidor"

        ),

        "Aplicação": (

            "processamento da aplicação",

            "após chegar ao servidor"

        ),

        "Transferência": (

            "transferência do conteúdo",

            "após chegar ao servidor"

        )

    }

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

        descricao, contexto = self.DESCRICOES.get(

            etapa,

            (

                etapa.lower(),

                ""

            )

        )

        return {

            "etapa": etapa,

            "descricao": descricao,

            "contexto": contexto,

            "tempo": tempo,

            "percentual": percentual,

            "ranking": ranking

        }