import sys


class Progress:

    WIDTH = 40

    def __init__(self):

        self.first_draw = True

        #
        # Quantidade de linhas impressas pelo painel
        #

        self.lines = 8

    def show(
        self,
        atual,
        total,
        destino,
        config
    ):

        percentual = int(

            (atual / total) * 100

        )

        preenchido = int(

            self.WIDTH * percentual / 100

        )

        barra = (

            "█" * preenchido +

            "░" * (self.WIDTH - preenchido)

        )

        #
        # Volta o cursor para o início do painel
        #

        if not self.first_draw:

            sys.stdout.write(f"\033[{self.lines}F")

        self.first_draw = False

        #
        # Limpa apenas as linhas do painel
        #

        for _ in range(self.lines):

            sys.stdout.write("\033[2K")
            sys.stdout.write("\033[1E")

        #
        # Volta novamente ao topo do painel
        #

        sys.stdout.write(f"\033[{self.lines}F")

        #
        # Desenha
        #

        print("=" * 92)
        print("Coleta em andamento".center(92))
        print("=" * 92)
        print()

        print(f"{barra} {percentual}%")
        print()

        print(f"Execução.............: {atual} de {total}")
        print()

        print("Aguarde...")

        sys.stdout.flush()