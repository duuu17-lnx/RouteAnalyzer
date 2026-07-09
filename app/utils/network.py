import ipaddress


def is_ip(valor: str) -> bool:

    try:

        ipaddress.ip_address(valor)

        return True

    except ValueError:

        return False