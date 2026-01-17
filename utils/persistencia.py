import pandas as pd
from datetime import datetime
import os

def salvar_erros(erros, banca):
    if not erros:
        return None

    pasta = "log/erros"
    os.makedirs(pasta, exist_ok=True)

    arquivo = f"{pasta}/erros_{banca}.xlsx"

    registros = []

    for q in erros:
        registros.append({
            "Data": datetime.now().strftime("%d/%m/%Y"),
            "Banca": q["banca"],
            "Ano": q["ano"],
            "Matéria": q["materia"],
            "Enunciado": q["enunciado"],
            "Alternativa marcada": f"{q['marcada']}) {q['alternativas'][q['marcada']]}",
            "Alternativa correta": f"{q['correta']}) {q['alternativas'][q['correta']]}",
        }
        )

    df_novo = pd.DataFrame(registros)

    if os.path.exists(arquivo):
        df_antigo = pd.read_excel(arquivo)
        df_final = pd.concat([df_antigo, df_novo], ignore_index=True)
    else:
        df_final = df_novo

    df_final.to_excel(arquivo, index=False)
    return arquivo
