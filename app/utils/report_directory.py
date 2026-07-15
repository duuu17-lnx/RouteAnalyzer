from pathlib import Path
import os
import platform
import subprocess


class ReportDirectory:

    @staticmethod
    def get_directory():

        reports = (

            Path(__file__)

            .resolve()

            .parents[2]

            / "reports"

        )

        reports.mkdir(

            parents=True,

            exist_ok=True

        )

        return reports

    def open(self):

        reports = self.get_directory()

        print()

        print("=" * 92)
        print("Acessar Relatórios".center(92))
        print("=" * 92)
        print()

        print(f"Pasta: {reports}")

        sistema = platform.system()

        try:

            if sistema == "Windows":

                os.startfile(

                    reports

                )

            elif sistema == "Linux":

                subprocess.Popen(

                    [

                        "xdg-open",

                        str(reports)

                    ],

                    stdout=subprocess.DEVNULL,

                    stderr=subprocess.DEVNULL

                )

            elif sistema == "Darwin":

                subprocess.Popen(

                    [

                        "open",

                        str(reports)

                    ],

                    stdout=subprocess.DEVNULL,

                    stderr=subprocess.DEVNULL

                )

            else:

                raise RuntimeError(

                    "Sistema operacional não suportado."

                )

            print()

            print("✓ Diretório aberto com sucesso.")

        except Exception:

            print()

            print(

                "Não foi possível abrir automaticamente o diretório."

            )

            print()

            print(

                "Os relatórios estão disponíveis em:"

            )

            print()

            print(

                reports

            )

        print()

        input(

            "Pressione ENTER para retornar ao menu..."

        )