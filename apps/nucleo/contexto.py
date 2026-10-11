from apps.nucleo.dados_da_empresa import DADOS_DA_EMPRESA


def dados_da_empresa(request):
    """Disponibiliza os dados da empresa em todos os templates como `empresa`."""
    return {"empresa": DADOS_DA_EMPRESA}
