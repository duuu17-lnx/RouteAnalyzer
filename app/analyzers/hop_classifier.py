from app.analyzers.event_classifier import EventClassifier


class HopClassifier:

    def __init__(self):

        self.classifier = EventClassifier()

    def classify(self, hops):

        #
        # Primeiro ASN encontrado
        #

        primeiro_asn = ""

        for hop in hops:

            if hop.asn:

                primeiro_asn = hop.asn

                break

        ultimo_asn = primeiro_asn

        ultima_localizacao = ""

        #
        # Classificação
        #

        for indice, hop in enumerate(hops):

            #
            # Gateway
            #

            if indice == 0:

                hop.evento = "Gateway"

                hop.observacao = "Rede Local"

                if hop.localizacao:

                    ultima_localizacao = hop.localizacao

                continue

            #
            # Destino
            #

            if indice == len(hops) - 1:

                hop.evento = "Destino"

                hop.observacao = "Host Final"

                continue

            #
            # Detecta mudança de país
            #

            if hop.localizacao:

                if (

                    ultima_localizacao

                    and hop.localizacao != ultima_localizacao

                ):

                    hop.evento = "Internacional"

                    hop.observacao = (

                        f"{ultima_localizacao} → {hop.localizacao}"

                    )

                    ultima_localizacao = hop.localizacao

                    continue

                ultima_localizacao = hop.localizacao

            #
            # Sem ASN
            #

            if not hop.asn:

                continue

            #
            # Backbone próprio
            #

            if hop.asn == primeiro_asn:

                hop.evento = "Backbone Próprio"

                hop.observacao = hop.empresa

                ultimo_asn = hop.asn

                continue

            #
            # Mudança de ASN
            #

            if hop.asn != ultimo_asn:

                resultado = self.classifier.classify(hop)

                if resultado["evento"]:

                    hop.evento = resultado["evento"]

                    hop.observacao = resultado["observacao"]

                else:

                    hop.evento = "Troca de ASN"

                    hop.observacao = (

                        f"{ultimo_asn} → {hop.asn}"

                    )

                ultimo_asn = hop.asn

                continue

            #
            # Mesmo ASN
            #

            resultado = self.classifier.classify(hop)

            if resultado["evento"]:

                hop.evento = resultado["evento"]

                hop.observacao = resultado["observacao"]