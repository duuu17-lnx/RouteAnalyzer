class ToolError(RuntimeError):
    """
    Exceção utilizada para indicar falhas em ferramentas
    externas (MTR, curl, tracert, ping, etc.), permitindo
    exibir mensagens amigáveis ao usuário sem gerar traceback.
    """

    pass