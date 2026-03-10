import re

# --- VALIDAÇÕES DE DÍGITO VERIFICADOR ---

def validar_cnpj(cnpj):
    """Valida CNPJ com cálculo de dígitos verificadores e pesos oficiais."""
    cnpj = re.sub(r'\D', '', str(cnpj))
    if len(cnpj) != 14 or len(set(cnpj)) == 1: 
        return False
    
    def calc_digito(trecho, pesos):
        soma = sum(int(a) * b for a, b in zip(trecho, pesos))
        resto = soma % 11
        return '0' if resto < 2 else str(11 - resto)

    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    
    dg1 = calc_digito(cnpj[:12], pesos1)
    dg2 = calc_digito(cnpj[:13], pesos2)
    
    return cnpj[-2:] == dg1 + dg2

def validar_cpf(cpf):
    """Valida CPF com cálculo de dígitos verificadores."""
    cpf = re.sub(r'\D', '', str(cpf))
    if len(cpf) != 11 or cpf == cpf[0] * 11: 
        return False
    
    for i in range(9, 11):
        soma = sum(int(cpf[num]) * ((i + 1) - num) for num in range(0, i))
        digito = ((soma * 10) % 11) % 10
        if digito != int(cpf[i]): 
            return False
    return True

# --- FORMATAÇÃO VISUAL (MÁSCARAS PARA O BACKEND) ---

def formatar_cnpj(v):
    v = re.sub(r'\D', '', str(v))
    if len(v) != 14: return v
    return f"{v[:2]}.{v[2:5]}.{v[5:8]}/{v[8:12]}-{v[12:]}"

def formatar_cpf(v):
    v = re.sub(r'\D', '', str(v))
    if len(v) != 11: return v
    return f"{v[:3]}.{v[3:6]}.{v[6:9]}-{v[9:]}"

def formatar_cep(v):
    v = re.sub(r'\D', '', str(v))
    if len(v) != 8: return v
    return f"{v[:5]}-{v[5:]}"

def formato_moeda(valor):
    """Converte float para R$ 0.000,00"""
    if valor is None: return "R$ 0,00"
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def formato_data(data_str):
    """Converte AAAA-MM-DD para DD/MM/AAAA"""
    if not data_str: return ""
    try:
        partes = data_str.split('-')
        return f"{partes[2]}/{partes[1]}/{partes[0]}"
    except:
        return data_str