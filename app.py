import streamlit as st
from dados.questoes import QUESTOES
from utils.persistencia import salvar_erros

st.set_page_config(page_title="Caderno de Erros - Provas Concursos")
st.title("Caderno de Erros - Provas Concursos")

# =========================
# Seleção de banca
# =========================
bancas = sorted(list(set(q["banca"] for q in QUESTOES)))
banca_escolhida = st.selectbox("Escolha a banca", bancas)

# =========================
# Inicialização / reset ao trocar banca
# =========================
if "banca_atual" not in st.session_state or st.session_state.banca_atual != banca_escolhida:
    st.session_state.banca_atual = banca_escolhida
    st.session_state.indice = 0
    st.session_state.erros = []
    st.session_state.confirmada = False
    st.session_state.resposta = None
    st.session_state.feedback = None
    st.session_state.questoes_filtradas = [
        q for q in QUESTOES if q["banca"] == banca_escolhida
    ]

questoes = st.session_state.questoes_filtradas

# =========================
# Simulado
# =========================
if st.session_state.indice < len(questoes):
    q = questoes[st.session_state.indice]

    st.markdown(f"### Questão {st.session_state.indice + 1}/{len(questoes)}")
    st.markdown(f"**{q['banca']} | {q['ano']} | {q['materia']}**")
    st.markdown(q["enunciado"])

    alternativas_formatadas = [
        f"{letra}) {texto}" for letra, texto in q["alternativas"].items()
    ]

    # =========================
    # FORM (resolve o duplo clique no Cloud)
    # =========================
    if not st.session_state.confirmada:
        with st.form(key=f"form_{st.session_state.indice}"):
            st.session_state.resposta = st.radio(
                "Escolha a resposta",
                alternativas_formatadas
            )

            submit = st.form_submit_button("Confirmar Resposta")

        if submit:
            st.session_state.confirmada = True
            resposta_letra = st.session_state.resposta.split(")")[0]

            if resposta_letra != q["correta"]:
                erro = q.copy()
                erro["marcada"] = resposta_letra
                st.session_state.erros.append(erro)

                st.session_state.feedback = (
                    "erro",
                    f"❌ Errado! A correta é: {q['correta']}) {q['alternativas'][q['correta']]}"
                )
            else:
                st.session_state.feedback = ("acerto", "✅ Acertou!")

            st.rerun()

    else:
        # Feedback
        tipo, msg = st.session_state.feedback
        if tipo == "erro":
            st.error(msg)
        else:
            st.success(msg)

        # Próxima questão
        if st.button("Próxima Questão"):
            st.session_state.indice += 1
            st.session_state.confirmada = False
            st.session_state.resposta = None
            st.session_state.feedback = None
            st.rerun()

# =========================
# Final do simulado
# =========================
else:
    st.success("🎉 Simulado concluído!")
    st.info(f"Você errou {len(st.session_state.erros)} questões.")

    salvar_erros(st.session_state.erros, banca_escolhida)
    st.info(f"Caderno de erros salvo em log/erros/erros_{banca_escolhida}.txt")

    if st.button("🔄 Reiniciar Simulado"):
        st.session_state.indice = 0
        st.session_state.erros = []
        st.session_state.confirmada = False
        st.session_state.resposta = None
        st.session_state.feedback = None
        st.rerun()
