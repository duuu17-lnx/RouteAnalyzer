from app.dns.dns_collector_factory import DNSCollectorFactory


class ApplicationDNS:

    DEFAULT_DNS = {

        "origem": "Padrão",

        "nome": "G6 Primário",

        "ip": "201.159.154.3"

    }

    def resolve(

        self,

        dominio,

        dns=None

    ):

        #
        # Utiliza o DNS padrão
        #

        if dns is None:

            dns = self.DEFAULT_DNS

        #
        # Usuário informou apenas um IP
        #

        elif isinstance(

            dns,

            str

        ):

            dns = {

                "origem": "Personalizado",

                "nome": dns,

                "ip": dns

            }

        collector = DNSCollectorFactory().get()

        return collector.query(

            dominio,

            dns

        )