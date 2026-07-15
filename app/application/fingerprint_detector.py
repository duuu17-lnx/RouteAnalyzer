class FingerprintDetector:

    def detect(self, headers):

        if not headers:

            return None

        #
        # Todos em minúsculo
        #

        h = {

            k.lower(): str(v).lower()

            for k, v in headers.items()

        }

        #
        # Server
        #

        server = h.get(

            "server",

            ""

        )

        #
        # Cloudflare
        #

        if (

            "cf-ray" in h or

            "cf-cache-status" in h or

            "cloudflare" in server

        ):

            return {

                "fabricante": "Cloudflare",

                "produto": "Cloudflare",

                "categoria": "CDN / WAF"

            }

        #
        # Amazon CloudFront
        #

        if (

            "x-amz-cf-id" in h or

            "x-amz-cf-pop" in h

        ):

            return {

                "fabricante": "Amazon",

                "produto": "CloudFront",

                "categoria": "CDN"

            }

        #
        # Fastly
        #

        if (

            "x-fastly-request-id" in h or

            "fastly" in h.get("via", "")

        ):

            return {

                "fabricante": "Fastly",

                "produto": "Fastly",

                "categoria": "CDN"

            }

        #
        # Akamai
        #

        if (

            "akamai" in str(h) or

            "x-akamai" in h

        ):

            return {

                "fabricante": "Akamai",

                "produto": "Akamai",

                "categoria": "CDN"

            }

        #
        # Imperva
        #

        if (

            "x-iinfo" in h or

            "visid_incap" in str(h) or

            "incapsula" in str(h)

        ):

            return {

                "fabricante": "Imperva",

                "produto": "Incapsula",

                "categoria": "WAF"

            }

        #
        # F5
        #

        if (

            "bigipserver" in str(h)

        ):

            return {

                "fabricante": "F5",

                "produto": "BIG-IP",

                "categoria": "Load Balancer"

            }

        #
        # HAProxy
        #

        if "haproxy" in server:

            return {

                "fabricante": "HAProxy",

                "produto": "HAProxy",

                "categoria": "Reverse Proxy"

            }

        #
        # NGINX
        #

        if "nginx" in server:

            return {

                "fabricante": "NGINX",

                "produto": "NGINX",

                "categoria": "Web Server"

            }

        #
        # OpenResty
        #

        if "openresty" in server:

            return {

                "fabricante": "OpenResty",

                "produto": "OpenResty",

                "categoria": "Reverse Proxy"

            }

        #
        # Apache
        #

        if "apache" in server:

            return {

                "fabricante": "Apache",

                "produto": "HTTP Server",

                "categoria": "Web Server"

            }

        #
        # LiteSpeed
        #

        if "litespeed" in server:

            return {

                "fabricante": "LiteSpeed",

                "produto": "LiteSpeed",

                "categoria": "Web Server"

            }

        #
        # Microsoft IIS
        #

        if "microsoft-iis" in server:

            return {

                "fabricante": "Microsoft",

                "produto": "IIS",

                "categoria": "Web Server"

            }

        #
        # Caddy
        #

        if "caddy" in server:

            return {

                "fabricante": "Caddy",

                "produto": "Caddy",

                "categoria": "Web Server"

            }

        #
        # Envoy
        #

        if "envoy" in server:

            return {

                "fabricante": "Envoy",

                "produto": "Envoy",

                "categoria": "Proxy"

            }

        #
        # Traefik
        #

        if "traefik" in server:

            return {

                "fabricante": "Traefik",

                "produto": "Traefik",

                "categoria": "Reverse Proxy"

            }

        #
        # Varnish
        #

        if (

            "varnish" in h.get("via", "") or

            "varnish" in str(h)

        ):

            return {

                "fabricante": "Varnish",

                "produto": "Varnish Cache",

                "categoria": "HTTP Cache"

            }

        #
        # Não identificado
        #

        return None