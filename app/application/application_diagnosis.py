class ApplicationDiagnosis:

    HTTP_STATUS = {

        200: "OK",

        301: "Moved Permanently",

        302: "Found",

        400: "Bad Request",

        401: "Unauthorized",

        403: "Forbidden",

        404: "Not Found",

        408: "Request Timeout",

        429: "Too Many Requests",

        500: "Internal Server Error",

        502: "Bad Gateway",

        503: "Service Unavailable",

        504: "Gateway Timeout"

    }

    def build(

        self,

        resultado,

        responsabilidade,

        estatisticas

    ):

        #
        # Organização do diagnóstico
        #

        conectividade = []

        desempenho = []

        aplicacao = []

        observacoes = []

        detalhes = []

        #
        # Resultado efetivo
        #

        ultimo = resultado.get_final()

        #
        # Nenhuma execução válida
        #

        if estatisticas["validas"] == 0:

            detalhes.append(

                f"Foram realizadas {estatisticas['execucoes']} requisições HTTP independentes."

            )

            detalhes.append(

                "Nenhuma das requisições HTTP pôde ser concluída."

            )

            if responsabilidade["DNS"] == "Falha":

                conectividade.append(

                    "Há indícios de falha na resolução DNS."

                )

                detalhes.append(

                    "O domínio não pôde ser resolvido pelo resolvedor DNS utilizado."

                )

                detalhes.append(

                    "As etapas TCP, TLS e aplicação não puderam ser avaliadas."

                )

            elif responsabilidade["Rede"] in (

                "Falha",

                "Timeout"

            ):

                conectividade.append(

                    "Há indícios de falha de conectividade entre a estação e o servidor remoto."

                )

                detalhes.append(

                    "Não foi possível estabelecer conectividade TCP com o servidor remoto."

                )

                detalhes.append(

                    "As etapas TLS e aplicação não puderam ser avaliadas."

                )

            elif responsabilidade["TLS"] == "Falha":

                conectividade.append(

                    "Foi observada falha durante o estabelecimento da conexão segura (TLS)."

                )

                detalhes.append(

                    "A conexão TCP foi estabelecida, porém o handshake TLS falhou."

                )

                detalhes.append(

                    "A aplicação não pôde ser avaliada."

                )

            else:

                aplicacao.append(

                    "Não foi possível concluir o diagnóstico da aplicação."

                )

            return (

                conectividade

                + desempenho

                + aplicacao

                + observacoes

                + detalhes

            )

        #
        # Conclusão de conectividade
        #

        if responsabilidade["DNS"] != "OK":

            conectividade.append(

                "Há indícios de falha na resolução DNS."

            )

        elif responsabilidade["Rede"] not in (

            "OK",

            "Não testada"

        ):

            conectividade.append(

                "Há indícios de falha de conectividade entre a estação e o servidor remoto."

            )

        elif responsabilidade["TLS"] not in (

            "OK",

            "Não testado"

        ):

            conectividade.append(

                "Foi observada falha durante o estabelecimento da conexão segura (TLS)."

            )

        else:

            conectividade.append(

                "Os testes realizados não indicam limitação de conectividade entre a estação e o servidor remoto."

            )

        #
        # Conclusão de desempenho
        #

        desempenho_info = estatisticas.get(

            "desempenho"

        )

        if desempenho_info:

            etapa = desempenho_info.get(

                "etapa",

                ""

            )

            if etapa:

                if etapa in (

                    "DNS",

                    "TCP",

                    "TLS"

                ):

                    desempenho.append(

                        "A maior parte do tempo da requisição foi consumida antes de chegar ao servidor (ANTES DE CHEGAR AO SERVIDOR)."

                    )

                else:

                    desempenho.append(

                        "A maior parte do tempo da requisição foi consumida durante a transferência (DEPOIS DE CHEGAR AO SERVIDOR)."

                    )

        if resultado.redirect:

            observacoes.append(

                "A análise de desempenho considera o recurso final obtido após todos os redirecionamentos HTTP."

            )

        #
        # Conclusão da aplicação
        #

        status = responsabilidade["Aplicação"]
        if status == "OK":

            aplicacao.append(

                "Não foram observados indícios de indisponibilidade da aplicação."

            )

            aplicacao.append(

                "Não há indícios de falha na rede do provedor."

            )

        elif status == "Redirect":

            aplicacao.append(

                "Não foram observados indícios de indisponibilidade da aplicação."

            )

            aplicacao.append(

                "Não há indícios de falha na rede do provedor."

            )

            observacoes.append(

                "A URL solicitada realizou redirecionamento HTTP de forma esperada."

            )

            observacoes.append(

                "O conteúdo foi entregue com sucesso pelo destino efetivo."

            )

        elif status == "Indisponível":

            aplicacao.append(

                "Há fortes indícios de indisponibilidade da aplicação remota."

            )

            detalhes.append(

                "O servidor respondeu com HTTP 503 Service Unavailable."

            )

        elif status == "Restrição":

            aplicacao.append(

                "A conectividade ocorreu normalmente, porém o acesso foi negado pela aplicação."

            )

            detalhes.append(

                "O servidor recusou a requisição (HTTP 403 Forbidden)."

            )

        elif status == "Recurso":

            aplicacao.append(

                "A conectividade ocorreu normalmente, porém o recurso solicitado não existe ou não está disponível."

            )

            detalhes.append(

                "O recurso solicitado não foi encontrado (HTTP 404 Not Found)."

            )

        elif status == "Erro":

            aplicacao.append(

                "A aplicação respondeu com erro interno."

            )

        else:

            aplicacao.append(

                "A aplicação apresentou comportamento diferente do esperado."

            )

        #
        # Detalhes técnicos
        #

        detalhes.append(

            f"Foram realizadas {estatisticas['execucoes']} requisições HTTP independentes."

        )

        if estatisticas["intermitencia"]:

            detalhes.append(

                "Foi observado comportamento intermitente entre as execuções."

            )

        else:

            detalhes.append(

                "Todas as execuções apresentaram comportamento consistente."

            )

        http_original = estatisticas.get(

            "http_original",

            {}

        )

        if http_original:

            if len(http_original) == 1:

                codigo = next(

                    iter(http_original)

                )

                quantidade = http_original[codigo]

                descricao = self.HTTP_STATUS.get(

                    codigo,

                    ""

                )

                texto = f"HTTP {codigo}"

                if descricao:

                    texto += f" {descricao}"

                detalhes.append(

                    f"A URL informada respondeu {texto} em todas as {quantidade} execuções."

                )

            else:

                respostas = []

                for codigo, quantidade in sorted(

                    http_original.items()

                ):

                    descricao = self.HTTP_STATUS.get(

                        codigo,

                        ""

                    )

                    texto = f"HTTP {codigo}"

                    if descricao:

                        texto += f" {descricao}"

                    respostas.append(

                        f"{texto}: {quantidade}"

                    )

                detalhes.append(

                    "A URL original apresentou diferentes respostas HTTP "

                    f"({', '.join(respostas)})."

                )

        http_final = estatisticas.get(

            "http_final",

            {}

        )

        if http_final:

            if len(http_final) == 1:

                codigo = next(

                    iter(http_final)

                )

                quantidade = http_final[codigo]

                descricao = self.HTTP_STATUS.get(

                    codigo,

                    ""

                )

                texto = f"HTTP {codigo}"

                if descricao:

                    texto += f" {descricao}"

                if http_final != http_original:

                    detalhes.append(

                        f"Após os redirecionamentos, o destino final respondeu {texto} em todas as {quantidade} execuções."

                    )

            else:

                respostas = []

                for codigo, quantidade in sorted(

                    http_final.items()

                ):

                    descricao = self.HTTP_STATUS.get(

                        codigo,

                        ""

                    )

                    texto = f"HTTP {codigo}"

                    if descricao:

                        texto += f" {descricao}"

                    respostas.append(

                        f"{texto}: {quantidade}"

                    )

                detalhes.append(

                    "O destino final apresentou diferentes respostas HTTP "

                    f"({', '.join(respostas)})."

                )

        #
        # Ordem final do diagnóstico
        #

        return (

            conectividade

            + desempenho

            + aplicacao

            + observacoes

            + detalhes

        )