from datetime import datetime


def mostrar_header(trace):

    print("=" * 92)
    print(" " * 38 + "RouteAnalyzer")
    print("=" * 92)
    print()

    print(f"Origem.........: {trace.origem}")
    print(f"Destino........: {trace.destino}")
    print(f"IP.............: {trace.destino_ip}")

    if trace.destino_asn:

        print(
            f"ASN Destino....: AS{trace.destino_asn} ({trace.destino_empresa})"
        )

    else:

        print("ASN Destino....: Não identificado")

    print(
        "Data...........:",
        datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    )

    print()