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

        diagnostico = []

        #
        # Resultado efetivo da requisição
        #

        ultimo = resultado.get_final()

        #
        # Quantidade de execuções
        #

        diagnostico.append(

            f"Foram realizadas {estatisticas['execucoes']} requisições HTTP independentes."

        )

        #
        # Nenhuma execução válida
        #

        if estatisticas["validas"] == 0:

            diagnostico.append(

                "Nenhuma das requisições HTTP pôde ser concluída."

            )

            if responsabilidade["DNS"] == "Falha":

                diagnostico.append(

                    "O domínio não pôde ser resolvido pelo resolvedor DNS utilizado."

                )

                diagnostico.append(

                    "As etapas de conectividade TCP, TLS e aplicação não puderam ser avaliadas."

                )

            elif responsabilidade["Rede"] in (

                "Falha",

                "Timeout"

            ):

                diagnostico.append(

                    "Não foi possível estabelecer conectividade TCP com o servidor remoto."

                )

                diagnostico.append(

                    "As etapas TLS e aplicação não puderam ser avaliadas."

                )

            elif responsabilidade["TLS"] == "Falha":

                diagnostico.append(

                    "A conexão TCP foi estabelecida, porém o handshake TLS falhou."

                )

                diagnostico.append(

                    "A aplicação não pôde ser avaliada."

                )

            else:

                diagnostico.append(

                    "Não foi possível concluir o diagnóstico da aplicação."

                )

            return diagnostico

        #
        # Consistência
        #

        if estatisticas["intermitencia"]:

            diagnostico.append(

                "Foi observado comportamento intermitente entre as execuções."

            )

        else:

            diagnostico.append(

                "Todas as execuções apresentaram comportamento consistente."

            )

        #
        # HTTP ORIGINAL
        #

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

                diagnostico.append(

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

                diagnostico.append(

                    "A URL original apresentou diferentes respostas HTTP "

                    f"({', '.join(respostas)})."

                )

        #
        # HTTP FINAL
        #

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

                    diagnostico.append(

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

                diagnostico.append(

                    "O destino final apresentou diferentes respostas HTTP "

                    f"({', '.join(respostas)})."

                )

        #
        # DNS
        #

        if responsabilidade["DNS"] != "OK":

            diagnostico.append(

                "Há indícios de falha na resolução DNS."

            )

            return diagnostico

        #
        # Rede
        #

        if responsabilidade["Rede"] not in (

            "OK",

            "Não testada"

        ):

            diagnostico.append(

                "Há indícios de falha de conectividade entre a estação e o servidor remoto."

            )

            return diagnostico

        #
        # TLS
        #

        if responsabilidade["TLS"] not in (

            "OK",

            "Não testado"

        ):

            diagnostico.append(

                "Foi observada falha durante o estabelecimento da conexão segura (TLS)."

            )

            return diagnostico

        #
        # Aplicação
        #

        status = responsabilidade["Aplicação"]

        if status == "OK":

            diagnostico.append(

                "Não foram observados indícios de indisponibilidade da aplicação."

            )

            diagnostico.append(

                "Não há indícios de falha na rede do provedor."

            )

        elif status == "Redirect":

            diagnostico.append(

                "A URL solicitada realizou redirecionamento HTTP de forma esperada."

            )

            diagnostico.append(

                "O conteúdo foi entregue com sucesso pelo destino efetivo."

            )

            diagnostico.append(

                "Não foram observados indícios de indisponibilidade da aplicação."

            )

            diagnostico.append(

                "Não há indícios de falha na rede do provedor."

            )

        elif status == "Indisponível":

            diagnostico.append(

                "O servidor respondeu com HTTP 503 Service Unavailable."

            )

            diagnostico.append(

                "Há fortes indícios de indisponibilidade da aplicação remota."

            )

        elif status == "Restrição":

            diagnostico.append(

                "O servidor recusou a requisição (HTTP 403 Forbidden)."

            )

            diagnostico.append(

                "A conectividade ocorreu normalmente, porém o acesso foi negado pela aplicação."

            )

        elif status == "Recurso":

            diagnostico.append(

                "O recurso solicitado não foi encontrado (HTTP 404 Not Found)."

            )

            diagnostico.append(

                "A conectividade ocorreu normalmente, porém o recurso solicitado não existe ou não está disponível."

            )

        elif status == "Erro":

            diagnostico.append(

                "A aplicação respondeu com erro interno."

            )

        else:

            diagnostico.append(

                "A aplicação apresentou comportamento diferente do esperado."

            )

        return diagnostico