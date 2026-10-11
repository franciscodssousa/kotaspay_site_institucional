"""
Dados da empresa exibidos nas páginas legais (Política de Privacidade,
Termos de Uso e LGPD).
Item vazio ("")  => a página legal o mostra destacado em amarelo como pendente 
pois não está preseente e com valor diferente de vazio  no dicionario 'DADOS_DA_EMPRESA' abaixo.
"""

DADOS_DA_EMPRESA = {
    "razao_social": "",
    "cnpj": "",
    "endereco": "",
    "nome_do_encarregado": "",
    "email_do_encarregado": "",
    "email_de_contato": "",
    "foro": "",  # ex.: "Fortaleza/CE"
    "prazo_de_retencao": "",  # ex.: "12 meses"
    "data_de_atualizacao": "",  # ex.: "11/10/2026"
}
