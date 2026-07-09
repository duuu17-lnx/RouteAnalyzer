class ASNAnalyzer:

    def analyze(self, trace):

        asns = []

        primeiro_asn = None
        primeira_empresa = None

        for hop in trace.hops:

            if not hop.asn:
                continue

            if primeiro_asn is None:
                primeiro_asn = hop.asn
                primeira_empresa = hop.empresa

            if hop.asn not in asns:
                asns.append(hop.asn)

        return {

            "asn_origem": primeiro_asn,

            "empresa_origem": primeira_empresa,

            "total_asns": len(asns)

        }