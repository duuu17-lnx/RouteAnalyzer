class DNSAnalyzer:

    def analyze(self, resultados):

        conclusoes = []

        #
        # Domínio inexistente
        #

        if resultados and all(

            dns.status == "NXDOMAIN"

            for dns in resultados

        ):

            conclusoes.append(

                "O domínio informado não existe (NXDOMAIN)."

            )

            return conclusoes

        #
        # Todos recusaram
        #

        if resultados and all(

            dns.status == "REFUSED"

            for dns in resultados

        ):

            conclusoes.append(

                "Todos os resolvedores recusaram a consulta."

            )

            return conclusoes

        #
        # Todos SERVFAIL
        #

        if resultados and all(

            dns.status == "SERVFAIL"

            for dns in resultados

        ):

            conclusoes.append(

                "Todos os resolvedores retornaram SERVFAIL."

            )

            conclusoes.append(

                "Há indícios de falha na resolução DNS."

            )

            return conclusoes

        #
        # Classifica desempenho
        #

        for dns in resultados:

            if dns.status != "OK":

                continue

            if dns.tempo <= 30:

                dns.status = "OK"

            elif dns.tempo <= 100:

                dns.status = "Lento"

            else:

                dns.status = "Muito Lento"

        #
        # Separa grupos
        #

        local = next(

            (d for d in resultados if d.origem == "Local"),

            None

        )

        internos = [

            d

            for d in resultados

            if d.origem == "Interno"

        ]

        publicos = [

            d

            for d in resultados

            if d.origem == "Público"

        ]

        #
        # Todos OK
        #

        if all(

            d.status == "OK"

            for d in resultados

        ):

            conclusoes.append(

                "Todos os resolvedores responderam normalmente."

            )

        #
        # DNS Local
        #

        if local:

            if local.status in (

                "Timeout",

                "Erro",

                "SERVFAIL",

                "REFUSED"

            ):

                if all(

                    d.status == "OK"

                    for d in internos + publicos

                ):

                    conclusoes.append(

                        "O resolvedor configurado localmente apresentou falha."

                    )

                    conclusoes.append(

                        "Os demais resolvedores responderam normalmente."

                    )

                    conclusoes.append(

                        "Há indícios de problema na configuração DNS desta estação."

                    )

            elif local.status in (

                "Lento",

                "Muito Lento"

            ):

                conclusoes.append(

                    "O resolvedor configurado localmente apresentou tempo de resposta elevado."

                )

        #
        # Internos
        #

        internos_ok = [

            d

            for d in internos

            if d.status == "OK"

        ]

        internos_falha = [

            d

            for d in internos

            if d.status not in (

                "OK",

                "Lento",

                "Muito Lento"

            )

        ]

        if len(internos_falha) == len(internos):

            conclusoes.append(

                "Nenhum resolvedor interno respondeu corretamente."

            )

            if all(

                d.status == "OK"

                for d in publicos

            ):

                conclusoes.append(

                    "Todos os resolvedores públicos responderam normalmente."

                )

                conclusoes.append(

                    "Há fortes indícios de indisponibilidade da infraestrutura DNS interna."

                )

        elif len(internos_falha) == 1:

            conclusoes.append(

                f"O resolvedor {internos_falha[0].nome} apresentou falha."

            )

        elif len(internos_falha) > 1:

            conclusoes.append(

                f"{len(internos_falha)} resolvedores internos apresentaram falha."

            )

        #
        # Públicos
        #

        publicos_falha = [

            d

            for d in publicos

            if d.status not in (

                "OK",

                "Lento",

                "Muito Lento"

            )

        ]

        if publicos_falha:

            conclusoes.append(

                f"{len(publicos_falha)} resolvedores públicos apresentaram falha."

            )

        #
        # Lentidão
        #

        lentos = [

            d

            for d in resultados

            if d.status in (

                "Lento",

                "Muito Lento"

            )

        ]

        if lentos:

            nomes = ", ".join(

                d.nome

                for d in lentos

            )

            conclusoes.append(

                f"Resolvedores com tempo elevado: {nomes}."

            )

        #
        # Consistência das respostas
        #

        respostas = {

            d.resposta

            for d in resultados

            if d.resposta

        }

        if len(respostas) == 1:

            conclusoes.append(

                "Todos os resolvedores retornaram o mesmo endereço IPv4."

            )

        elif len(respostas) > 1:

            conclusoes.append(

                "Foram observadas respostas diferentes entre os resolvedores."

            )

            conclusoes.append(

                "Esse comportamento pode ser esperado em serviços com CDN ou balanceamento geográfico."

            )

        #
        # Nenhuma conclusão
        #

        if not conclusoes:

            conclusoes.append(

                "Não foram identificadas anormalidades relevantes."

            )

        return conclusoes