# funções de revisão e caderno de erros
from services.aplicador import aplicar_questao

def executar_simulado(questoes):
    erros = []

    for q in questoes:
        acertou, marcada = aplicar_questao(q)
        if not acertou:
            erro = q.copy()
            erro["marcada"] = marcada
            erros.append(erro)

    return erros
