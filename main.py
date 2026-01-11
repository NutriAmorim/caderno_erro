# arquivo principal que executa o sistema
from dados.questoes import QUESTOES
from services.filtros import listar_bancas, filtrar_por_banca
from services.revisao import executar_simulado
from utils.persistencia import salvar_erros

# 1. Escolher a banca
bancas = listar_bancas(QUESTOES)
print("Escolha a banca:")
for i, banca in enumerate(bancas, 1):
    print(f"{i} - {banca}")

opcao = int(input("Opção: "))
banca_escolhida = bancas[opcao - 1]

# 2. Filtrar questões da banca
questoes_banca = filtrar_por_banca(QUESTOES, banca_escolhida)

# 3. Executar simulado
erros = executar_simulado(questoes_banca)

# 4. Revisão dos erros
if erros:
    print("\nRevisão das questões que você errou:")
    for q in erros:
        # Reaplicar cada questão errada
        from services.aplicador import aplicar_questao
        aplicar_questao(q)
else:
    print("\nParabéns, você acertou todas!")

# 5. Salvar caderno de erros
salvar_erros(erros, banca_escolhida)

print(f"\nCaderno de erros salvo em log/erros/erros_{banca_escolhida}.txt")
