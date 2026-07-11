from dataclasses import dataclass


@dataclass
class AnalysisConfig:

    #
    # Perfil
    #

    perfil: str = "Padrão"

    #
    # Coleta
    #

    execucoes: int = 3

    ciclos: int = 80