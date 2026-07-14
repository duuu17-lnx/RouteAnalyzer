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
        # Classificação apenas informativa
        #

        for dns in resultados:

            if dns.status != "OK":

                continue

            if dns.tempo <= 10:

                dns.status = "Excelente"

            elif dns.tempo <= 25:

                dns.status = "Muito Bom"

            elif dns.tempo <= 50:

                dns.status = "Bom"

            elif dns.tempo <= 100:

                dns.status = "Normal"

            elif dns.tempo <= 300:

                dns.status = "Elevado"

            else:

                dns.status = "Muito Elevado"

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
        # DNS local
        #

        if local:

            if local.status in (

                "Timeout",

                "Erro",

                "SERVFAIL",

                "REFUSED"

            ):

                conclusoes.append(

                    "O resolvedor configurado localmente não respondeu corretamente."

                )

        #
        # Falhas em resolvedores internos
        #

        internos_falha = [

            d

            for d in internos

            if d.status in (

                "Timeout",

                "Erro",

                "SERVFAIL",

                "REFUSED"

            )

        ]

        if len(internos_falha) == len(internos) and internos:

            conclusoes.append(

                "Nenhum resolvedor interno respondeu corretamente."

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
        # Falhas em resolvedores públicos
        #

        publicos_falha = [

            d

            for d in publicos

            if d.status in (

                "Timeout",

                "Erro",

                "SERVFAIL",

                "REFUSED"

            )

        ]

        if publicos_falha:

            conclusoes.append(

                f"{len(publicos_falha)} resolvedores públicos apresentaram falha."

            )

        #
        # Tempos muito elevados
        #

        elevados = [

            d

            for d in resultados

            if d.status == "Muito Elevado"

        ]

        if elevados:

            nomes = ", ".join(

                d.nome

                for d in elevados

            )

            conclusoes.append(

                f"Resolvedores com tempo de resolução muito elevado: {nomes}."

            )

        #
        # Todos responderam corretamente
        #

        if all(

            d.status in (

                "Excelente",

                "Muito Bom",

                "Bom",

                "Normal",

                "Elevado",

                "Muito Elevado"

            )

            for d in resultados

        ):

            conclusoes.append(

                "Todos os resolvedores responderam corretamente às consultas DNS."

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

                "Esse comportamento é esperado em serviços que utilizam CDN ou balanceamento geográfico."

            )

        #
        # Observação educativa
        #

        conclusoes.append(

            "O tempo de resolução DNS representa apenas o tempo necessário para traduzir um nome de domínio em endereço IP. Tempos mais elevados não indicam, por si só, problemas de desempenho da conexão."

        )

        #
        # Nenhuma conclusão
        #

        if not conclusoes:

            conclusoes.append(

                "Não foram identificadas anormalidades relevantes."

            )

        return conclusoes