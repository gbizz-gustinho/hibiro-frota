# utils/formatters.py

def formatar_valor_db(valor):
    """Converte '1.250,50' ou 'R$ 1.250,50' para 1250.50 (float)"""
    if not valor: return 0.0
    try:
        # Remove R$, espaços e pontos de milhar, troca vírgula por ponto
        limpo = str(valor).replace('R$', '').replace('.', '').replace(',', '.').strip()
        return float(limpo)
    except:
        return 0.0

def formatar_data_db(data_str):
    """Converte 'DD/MM/AAAA' para 'AAAA-MM-DD' para o SQLite"""
    if not data_str or '/' not in data_str: return None
    try:
        d, m, a = data_str.split('/')
        return f"{a}-{m}-{d}"
    except:
        return None

def formatar_taxa_db(valor):
    """Converte '10,5%' ou '10,5' para 10.5 (float)"""
    if not valor: return 0.0
    try:
        limpo = str(valor).replace('%', '').replace(',', '.').strip()
        return float(limpo)
    except:
        return 0.0