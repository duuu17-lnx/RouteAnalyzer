class PerformanceDiagnosis:

    def build(self, performance):

        diagnostico = []

        if not performance:

            return diagnostico

        etapa = performance["etapa"]

        percentual = performance["percentual"]

        tempo = performance["tempo"]

        #
        # DNS
        #

        if etapa == "DNS":

            diagnostico.append(

                f"A maior parte do tempo da requisição foi consumida durante a resolução DNS ({percentual:.1f}%)."

            )

            diagnostico.append(

                "Esse comportamento pode indicar latência elevada na resolução de nomes ou indisponibilidade parcial dos resolvedores configurados."

            )

        #
        # TCP
        #

        elif etapa == "TCP":

            diagnostico.append(

                f"A maior parte do tempo da requisição foi consumida durante o estabelecimento da conexão TCP ({percentual:.1f}%)."

            )

            diagnostico.append(

                "Esse comportamento pode indicar latência elevada entre o cliente e o servidor remoto."

            )

        #
        # TLS
        #

        elif etapa == "TLS":

            diagnostico.append(

                f"A maior parte do tempo da requisição foi consumida durante o estabelecimento da conexão TLS ({percentual:.1f}%)."

            )

            diagnostico.append(

                "Esse comportamento normalmente está relacionado ao handshake criptográfico ou ao processamento do servidor remoto."

            )

        #
        # Aplicação
        #

        elif etapa == "Aplicação":

            diagnostico.append(

                f"A maior parte do tempo da requisição foi consumida durante o processamento da aplicação ({percentual:.1f}%)."

            )

            diagnostico.append(

                "Há indícios de que o servidor remoto demorou para iniciar a geração da resposta."

            )

        #
        # Transferência
        #

        elif etapa == "Transferência":

            diagnostico.append(

                f"A maior parte do tempo da requisição foi consumida durante a transferência do conteúdo ({percentual:.1f}%)."

            )

            diagnostico.append(

                "Esse comportamento normalmente está relacionado ao volume de dados transferidos, utilização de cache, CDN ou processamento da aplicação, e não à conectividade da rede."

            )

        #
        # Informação complementar
        #

        diagnostico.append(

            f"A etapa predominante consumiu aproximadamente {tempo:.2f} ms."

        )

        return diagnostico