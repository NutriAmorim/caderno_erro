# função que aplica cada questão
def aplicar_questao(q):
    print("\n--------------------------------")
    print(f"{q['banca']} | {q['ano']} | {q['materia']}")
    print(q["enunciado"])

    for letra, texto in q["alternativas"].items():
        print(f"{letra}) {texto}")

    resposta = input("Resposta: ").strip().upper()
    return resposta == q["correta"], resposta