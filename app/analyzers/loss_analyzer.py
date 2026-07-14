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
        # Verifica se o destino realmente respondeu
        #

        if trace.hops:

            ultimo_hop = trace.hops[-1]

            if (

                ultimo_hop.host == trace.destino

                and

                ultimo_hop.perda_real

                and

                ultimo_hop.loss >= primeiro_hop.loss

            ):

                persistente = True

        return {

            "hop": primeiro_hop,

            "persistente": persistente

        }