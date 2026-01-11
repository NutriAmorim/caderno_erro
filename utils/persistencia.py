# funções para salvar o caderno de erros em arquivos

def salvar_erros(erros, banca):
    nome_arquivo = f"log/erros/erros_{banca}.txt"

    with open(nome_arquivo, "w", encoding="utf-8") as f:
        for q in erros:
            f.write(f"Banca: {q['banca']} | Ano: {q['ano']} | Matéria: {q['materia']}\n")
            f.write(q["enunciado"] + "\n")
            f.write(f"Sua resposta: {q['marcada']} | Correta: {q['correta']}\n")
            f.write("-" * 50 + "\n")
