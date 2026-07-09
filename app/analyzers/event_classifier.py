from app.utils.asn_database import ASN_DATABASE

class EventClassifier:

    REDES = {
        "GOOGLE": ("Rede Google", "Google"),
        "MICROSOFT": ("Rede Microsoft", "Microsoft"),
        "CLOUDFLARE": ("Rede Cloudflare", "Cloudflare"),
        "AMAZON": ("Rede AWS", "Amazon"),
        "AWS": ("Rede AWS", "Amazon"),
        "META": ("Rede Meta", "Meta"),
        "FACEBOOK": ("Rede Meta", "Meta"),
        "AKAMAI": ("Rede Akamai", "Akamai"),
        "FASTLY": ("Rede Fastly", "Fastly"),
    }

    TRANSITOS = {
        "LUMEN": "Lumen",
        "LEVEL3": "Lumen",
        "COGENT": "Cogent",
        "ARELION": "Arelion",
        "TELIA": "Telia",
        "TELIANET": "Telia",
        "NTT": "NTT",
        "GTT": "GTT",
        "PCCW": "PCCW",
        "ZAYO": "Zayo",
    }

    def classify(self, hop):

        #
        # Primeiro tenta identificar pelo ASN
        #

        if hop.asn in ASN_DATABASE:

            info = ASN_DATABASE[hop.asn]

            tipo = info["tipo"]
            nome = info["nome"]

            if tipo == "ix":

                return {
                    "evento": "IX.br",
                    "observacao": "Ponto de Troca de Tráfego"
                }

            if tipo == "transito":

                return {
                    "evento": "Trânsito",
                    "observacao": nome
                }

            if tipo == "conteudo":

                return {
                    "evento": f"Rede {nome}",
                    "observacao": nome
                }

        #
        # Fallback pela descrição da empresa
        #

        empresa = hop.empresa.upper()

        for chave, (evento, obs) in self.REDES.items():

            if chave in empresa:

                return {
                    "evento": evento,
                    "observacao": obs
                }

        for chave, nome in self.TRANSITOS.items():

            if chave in empresa:

                return {
                    "evento": "Trânsito",
                    "observacao": nome
                }

        return {
            "evento": "",
            "observacao": ""
        }