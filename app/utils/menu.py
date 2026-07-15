class Menu:

    def show(self):

        print()

        print("=" * 92)
        print("RouteAnalyzer".center(92))
        print("=" * 92)
        print()

        print("[1] Diagnóstico MTR")
        print("[2] Diagnóstico de Aplicação")
        print("[3] Exportar Relatório")
        print("[4] Acessar Relatórios")
        print("[0] Sair")
        print()

        return input("Opção: ").strip()