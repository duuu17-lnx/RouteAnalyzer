class Menu:

    def show(self):

        print()
        print("=" * 92)
        print("Escolha uma opção".center(92))
        print("=" * 92)
        print()

        print("[1] Nova análise")
        print("[2] Diagnóstico DNS")
        print("[3] Exportar relatório")
        print("[0] Sair")
        print()

        return input("Opção: ").strip()