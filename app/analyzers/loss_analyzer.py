class LossAnalyzer:

    def analyze(self, trace):

        primeiro_hop = None

        persistente = False

        #
        # Procura a primeira perda REAL
        #

        for hop in trace.hops:

            #
            # Ignora ICMP filtrado
            #

            if not hop.perda_real:
                continue

            if hop.loss > 0:

                primeiro_hop = hop
                break

        #
        # Não existe perda real
        #

        if primeiro_hop is None:

            return {
                "hop": None,
                "persistente": False
            }

        #
        # Verifica se a perda chegou ao destino
        #

        if trace.hops[-1].perda_real:

            if trace.hops[-1].loss >= primeiro_hop.loss:

                persistente = True

        return {
            "hop": primeiro_hop,
            "persistente": persistente
        }