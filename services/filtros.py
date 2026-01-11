 # funções que filtram questões por banca
def listar_bancas(questoes):
    return sorted(set(q["banca"] for q in questoes))

def filtrar_por_banca(questoes, banca):
    return [q for q in questoes if q["banca"] == banca]