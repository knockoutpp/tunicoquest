import streamlit as st
import json
import os

# Configurações de Estilo "Gamer Moderno"
st.set_page_config(page_title="Tunico Quest Online", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0c0e23; color: white; }
    .stProgress > div > div > div > div { background-image: linear-gradient(to right, #00ffcc, #ff00ff); }
    .card { 
        background-color: #1c203c; 
        padding: 15px; 
        border-radius: 15px; 
        border: 1px solid #00ffff;
        margin-bottom: 10px;
    }
    .metric-box {
        text-align: center;
        background: rgba(0, 255, 204, 0.1);
        padding: 20px;
        border-radius: 20px;
        border: 2px solid #00ffcc;
    }
    </style>
    """, unsafe_allow_html=True)

# Dados baseados na sua planilha
TAREFAS = [
    "📚 Dever de Casa", "🎓 Atenção na Aula",
    "🛡️ Comportamento", "🔇 Sem Palavrões",
    "🏠 Ajudar em Casa", "😴 Dormir no Horário"
]
DIAS = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
PONTOS_CICLO = [0, 1, 2, 5, -1, -2] # Ordem: Neutro -> Cumprida -> Excelente -> Perfeito -> Mau -> Palavrão

if 'dados' not in st.session_state:
    st.session_state.dados = {t: [0]*7 for t in TAREFAS}

# Cálculo de Pontos
total_xp = sum(sum(v) for v in st.session_state.dados.values())
meta = 100 # Meta para o Videogame

# --- TOPO DA DASHBOARD ---
st.title("🕹️ TUNICO QUEST: LEVEL UP")

col_avatar, col_progresso, col_meta = st.columns([1, 2, 1])

with col_avatar:
    # Boneco que muda de acordo com o XP
    if total_xp >= meta:
        st.markdown("<h1 style='font-size: 80px; text-align: center;'>👑</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'><b>LENDÁRIO!</b></p>", unsafe_allow_html=True)
    elif total_xp >= 20:
        st.markdown("<h1 style='font-size: 80px; text-align: center;'>😎</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'><b>GUERREIRO</b></p>", unsafe_allow_html=True)
    elif total_xp >= 0:
        st.markdown("<h1 style='font-size: 80px; text-align: center;'>👦</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'><b>INICIANTE</b></p>", unsafe_allow_html=True)
    else:
        st.markdown("<h1 style='font-size: 80px; text-align: center;'>👾</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'><b>VILÃO (CUIDADO!)</b></p>", unsafe_allow_html=True)

with col_progresso:
    st.write(f"### Objetivo: Vídeo Game 🎮")
    prog = min(max(total_xp/meta, 0.0), 1.0)
    st.progress(prog)
    st.write(f"Faltam **{meta - total_xp} XP** para o prêmio!")

with col_meta:
    st.markdown(f"""
        <div class='metric-box'>
            <p style='margin:0;'>XP ATUAL</p>
            <h1 style='margin:0; color:#00ffcc;'>{total_xp}</h1>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# --- GRID INTERATIVA ---
st.subheader("📅 Missões da Semana")
cols_h = st.columns([2] + [1]*7)
for i, d in enumerate(["Missão"] + DIAS):
    cols_h[i].write(f"**{d}**")

for tarefa in TAREFAS:
    cols = st.columns([2] + [1]*7)
    cols[0].markdown(f"<div class='card'>{tarefa}</div>", unsafe_allow_html=True)
    
    for i in range(7):
        valor = st.session_state.dados[tarefa][i]
        # Cor do botão muda se for positivo ou negativo
        tipo = "primary" if valor > 0 else "secondary"
        
        if cols[i+1].button(f"{valor}", key=f"{tarefa}_{i}", help="Clique para mudar o ponto"):
            # Ciclo de pontos ao clicar
            idx_atual = PONTOS_CICLO.index(valor)
            novo_valor = PONTOS_CICLO[(idx_atual + 1) % len(PONTOS_CICLO)]
            st.session_state.dados[tarefa][i] = novo_valor
            st.rerun()

if st.sidebar.button("🗑️ Reiniciar Tudo"):
    st.session_state.dados = {t: [0]*7 for t in TAREFAS}
    st.rerun()

st.sidebar.info("""
**Legenda de Cliques:**
- 0: Neutro
- 1: Cumprida
- 2: Excelente
- 5: Dia Perfeito!
- -1: Mau comportamento
- -2: Palavrão
""")
