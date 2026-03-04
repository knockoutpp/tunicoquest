import streamlit as st
from streamlit_javascript import st_javascript
import json

# Configuração Gamer
st.set_page_config(page_title="Tunico Quest 2.0", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0c0e23; color: white; }
    .stProgress > div > div > div > div { background-image: linear-gradient(to right, #00ffcc, #ff00ff); }
    .card { background-color: #1c203c; padding: 15px; border-radius: 15px; border: 1px solid #00ffff; margin-bottom: 10px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE MEMÓRIA (Local Storage) ---
def salvar_no_navegador(dados):
    js_code = f"localStorage.setItem('tunico_data', '{json.dumps(dados)}');"
    st_javascript(js_code)

def carregar_do_navegador():
    js_code = "localStorage.getItem('tunico_data');"
    result = st_javascript(js_code)
    if result:
        return json.loads(result)
    return None

# Inicialização das Tarefas
TAREFAS = ["📚 Dever de Casa", "🎓 Atenção na Aula", "🛡️ Comportamento", "🔇 Sem Palavrões", "🏠 Ajudar em Casa", "😴 Dormir no Horário"]
DIAS = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
VALORES = [0, 1, 2, 5, -1, -2]

# Carregar dados
dados_salvos = carregar_do_navegador()
if 'dados' not in st.session_state:
    st.session_state.dados = dados_salvos if dados_salvos else {t: [0]*7 for t in TAREFAS}

# --- INTERFACE ---
total_xp = sum(sum(v) for v in st.session_state.dados.values())
meta = 100

st.title("🕹️ TUNICO QUEST: CLOUD SAVE")

col_avatar, col_prog = st.columns([1, 3])

with col_avatar:
    # Boneco Interativo que muda com o XP
    emoji = "👦" if total_xp >= 0 else "👾"
    if total_xp >= meta: emoji = "👑"
    st.markdown(f"<h1 style='font-size: 100px; text-align: center;'>{emoji}</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>XP: {total_xp}</h3>", unsafe_allow_html=True)

with col_prog:
    st.write(f"### Missão: Conquistar o Vídeo Game 🎮")
    prog = min(max(total_xp/meta, 0.0), 1.0)
    st.progress(prog)
    st.write(f"Faltam **{meta - total_xp} XP** para o prémio!")

st.divider()

# Grid de Jogo
cols_h = st.columns([2] + [1]*7)
for i, d in enumerate(["MISSÃO"] + DIAS):
    cols_h[i].write(f"**{d}**")

for tarefa in TAREFAS:
    cols = st.columns([2] + [1]*7)
    cols[0].markdown(f"<div class='card'>{tarefa}</div>", unsafe_allow_html=True)
    
    for i in range(7):
        val = st.session_state.dados[tarefa][i]
        if cols[i+1].button(f"{val}", key=f"{tarefa}_{i}"):
            # Ciclo de pontos
            idx = VALORES.index(val)
            st.session_state.dados[tarefa][i] = VALORES[(idx + 1) % len(VALORES)]
            salvar_no_navegador(st.session_state.dados)
            st.rerun()

if st.sidebar.button("🗑️ REINICIAR TUDO"):
    st.session_state.dados = {t: [0]*7 for t in TAREFAS}
    salvar_no_navegador(st.session_state.dados)
    st.rerun()
