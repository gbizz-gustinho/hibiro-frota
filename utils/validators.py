import re

def validar_cpf(cpf: str) -> bool:
    cpf = re.sub(r'\D', '', cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    for i in range(9, 11):
        value = sum((int(cpf[num]) * ((i + 1) - num) for num in range(0, i)))
        digit = ((value * 10) % 11) % 10
        if digit != int(cpf[i]):
            return False
    return True

def validar_cnpj(cnpj: str) -> bool:
    cnpj = re.sub(r'\D', '', cnpj)
    if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
        return False
    
    def calcular_digito(cnpj, peso):
        soma = sum(int(a) * b for a, b in zip(cnpj, peso))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    
    dg1 = calcular_digito(cnpj[:12], pesos1)
    dg2 = calcular_digito(cnpj[:13], pesos2)
    return cnpj[-2:] == f"{dg1}{dg2}"

def validar_documento(doc: str) -> bool:
    """Detecta se é CPF ou CNPJ e valida o dígito verificador."""
    doc_limpo = re.sub(r'\D', '', doc)
    if len(doc_limpo) == 11:
        return validar_cpf(doc_limpo)
    elif len(doc_limpo) == 14:
        return validar_cnpj(doc_limpo)
    return False