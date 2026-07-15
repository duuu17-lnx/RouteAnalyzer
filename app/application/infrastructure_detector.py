class InfrastructureDetector:

    def detect(self, headers):

        #
        # Todos em minúsculo
        #

        h = {

            k.lower(): v.lower()

            for k, v in headers.items()

        }

        texto = " ".join(

            h.values()

        )

        #
        # Cloudflare
        #

        if "cf-ray" in h:

            return (

                "Cloudflare",

                "CDN"

            )

        #
        # AWS CloudFront
        #

        if "cloudfront" in texto:

            return (

                "AWS CloudFront",

                "CDN"

            )

        #
        # Akamai
        #

        if "akamai" in texto:

            return (

                "Akamai",

                "CDN"

            )

        #
        # Fastly
        #

        if "fastly" in texto:

            return (

                "Fastly",

                "CDN"

            )

        #
        # Varnish
        #

        if "varnish" in texto:

            return (

                "Varnish",

                "Cache"

            )

        #
        # nginx
        #

        if "nginx" in texto:

            return (

                "Nginx",

                "Servidor Web"

            )

        #
        # Apache
        #

        if "apache" in texto:

            return (

                "Apache",

                "Servidor Web"

            )

        #
        # IIS
        #

        if "microsoft-iis" in texto:

            return (

                "Microsoft IIS",

                "Servidor Web"

            )

        #
        # Envoy
        #

        if "envoy" in texto:

            return (

                "Envoy",

                "Proxy"

            )

        #
        # Traefik
        #

        if "traefik" in texto:

            return (

                "Traefik",

                "Proxy"

            )

        return (

            "",

            ""

        )