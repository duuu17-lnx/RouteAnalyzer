from collections import Counter
from statistics import mean


class ApplicationStatistics:

    def calculate(

        self,

        resultados

    ):

        if not resultados:

            return {

                "execucoes": 0,

                "validas": 0,

                "falhas": 0,

                "http": {},
                "http_original": {},
                "http_final": {},

                "intermitencia": None,

                "dns_media": 0.0,
                "dns_min": 0.0,
                "dns_max": 0.0,

                "tcp_media": 0.0,
                "tcp_min": 0.0,
                "tcp_max": 0.0,

                "tls_media": 0.0,
                "tls_min": 0.0,
                "tls_max": 0.0,

                "app_media": 0.0,
                "app_min": 0.0,
                "app_max": 0.0,

                "transfer_media": 0.0,
                "transfer_min": 0.0,
                "transfer_max": 0.0,

                "total_media": 0.0,
                "total_min": 0.0,
                "total_max": 0.0

            }

        #
        # Execuções válidas
        #

        originais = [

            r

            for r in resultados

            if r.curl_exit_code == 0

        ]

        falhas = len(resultados) - len(originais)

        #
        # Nenhuma execução válida
        #

        if not originais:

            return {

                "execucoes": len(resultados),

                "validas": 0,

                "falhas": falhas,

                "http": {},
                "http_original": {},
                "http_final": {},

                "intermitencia": None,

                "dns_media": 0.0,
                "dns_min": 0.0,
                "dns_max": 0.0,

                "tcp_media": 0.0,
                "tcp_min": 0.0,
                "tcp_max": 0.0,

                "tls_media": 0.0,
                "tls_min": 0.0,
                "tls_max": 0.0,

                "app_media": 0.0,
                "app_min": 0.0,
                "app_max": 0.0,

                "transfer_media": 0.0,
                "transfer_min": 0.0,
                "transfer_max": 0.0,

                "total_media": 0.0,
                "total_min": 0.0,
                "total_max": 0.0

            }

        #
        # Resultados finais
        #

        finais = [

            r.get_final()

            for r in originais

        ]

        #
        # HTTP ORIGINAL
        #

        http_original = Counter(

            r.http_code

            for r in originais

        )

        #
        # HTTP FINAL
        #

        http_final = Counter(

            r.http_code

            for r in finais

        )

        #
        # Compatibilidade
        #

        http = dict(

            http_original

        )

        #
        # Médias do destino efetivo
        #

        dns = [

            r.dns_time

            for r in finais

        ]

        tcp = [

            r.tcp_time

            for r in finais

        ]

        tls = [

            r.tls_time

            for r in finais

        ]

        app = [

            r.application_time

            for r in finais

        ]

        transferencia = [

            r.transfer_time

            for r in finais

        ]

        total = [

            r.total_time

            for r in finais

        ]

        #
        # Intermitência da resposta original
        #

        intermitencia = len(

            http_original

        ) > 1

        return {

            "execucoes": len(resultados),

            "validas": len(originais),

            "falhas": falhas,

            #
            # Compatibilidade
            #

            "http": http,

            #
            # HTTP
            #

            "http_original": dict(

                http_original

            ),

            "http_final": dict(

                http_final

            ),

            #
            # Consistência
            #

            "intermitencia": intermitencia,

            #
            # Médias
            #

            "dns_media": round(mean(dns), 2),
            "dns_min": round(min(dns), 2),
            "dns_max": round(max(dns), 2),

            "tcp_media": round(mean(tcp), 2),
            "tcp_min": round(min(tcp), 2),
            "tcp_max": round(max(tcp), 2),

            "tls_media": round(mean(tls), 2),
            "tls_min": round(min(tls), 2),
            "tls_max": round(max(tls), 2),

            "app_media": round(mean(app), 2),
            "app_min": round(min(app), 2),
            "app_max": round(max(app), 2),

            "transfer_media": round(mean(transferencia), 2),
            "transfer_min": round(min(transferencia), 2),
            "transfer_max": round(max(transferencia), 2),

            "total_media": round(mean(total), 2),
            "total_min": round(min(total), 2),
            "total_max": round(max(total), 2)

        }