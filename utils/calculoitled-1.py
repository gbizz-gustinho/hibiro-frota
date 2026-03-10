def calcular_predicao_pneu(id_pneu):
    conn = get_db()
    # Pega as duas últimas medições para calcular o desgaste real
    medicoes = conn.execute('''
        SELECT sulco_lido, km_veiculo_no_dia, data_medicao 
        FROM vei_pneu_medicoes 
        WHERE id_pneu = ? 
        ORDER BY data_medicao DESC LIMIT 2
    ''', (id_pneu,)).fetchall()

    if len(medicoes) < 2:
        return "Dados insuficientes para predição"

    m1, m2 = medicoes[0], medicoes[1] # m1 é a mais recente
    
    # 1. Quanto rodou e quanto gastou
    km_rodada = m1['km_veiculo_no_dia'] - m2['km_veiculo_no_dia']
    desgaste_mm = m2['sulco_lido'] - m1['sulco_lido']
    
    if desgaste_mm <= 0: return "Sem desgaste detectado"

    # 2. Taxa de consumo (KM por milímetro)
    km_por_mm = km_rodada / desgaste_mm
    
    # 3. Quanto resta de borracha "útil" (até 3mm de segurança)
    borracha_util = m1['sulco_lido'] - 3.0
    km_restante = borracha_util * km_por_mm
    
    # 4. Dias restantes (baseado na média de KM diária do caminhão)
    # Supondo média de 300km/dia
    dias_restantes = int(km_restante / 300)
    
    return f"{dias_restantes} dias"