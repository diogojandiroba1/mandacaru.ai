import streamlit as st
import pandas as pd

# ---------------------------------------------------
# FUNÇÃO PARA RENDERIZAR O MENU SUPERIOR
# ---------------------------------------------------
def top_menu(navigate_to):

    st.markdown("""
        <style>
            .top-menu-container {
                display: flex;
                justify-content: center;
                gap: 20px;
                margin-top: 10px;
                margin-bottom: 30px;
            }

            .nav-btn {
                background: transparent;
                border: 1px solid #555;
                padding: 10px 25px;
                border-radius: 10px;
                color: #ddd;
                font-size: 16px;
                cursor: pointer;
                transition: 0.2s;
            }

            .nav-btn:hover {
                border-color: #8BC34A;
                color: #8BC34A;
            }

            .nav-btn-active {
                background: #8BC34A;
                border: 1px solid #8BC34A;
                color: black;
                font-weight: 600;
            }
        </style>
    """, unsafe_allow_html=True)

    current = st.session_state.get("page", "dashboard")

    st.markdown("<div class='top-menu-container'>", unsafe_allow_html=True)

    # Lista de páginas e seus identificadores
    botoes = [
        ("Dashboard", "dashboard"),
        ("Diagnóstico", "diagnostico"),
        ("Predição", "predicao"),
        ("Propriedade", "propriedade"),
        ("Sair", "login")
    ]

    cols = st.columns(len(botoes), gap="small")

    for i, (label, target) in enumerate(botoes):
        classe = "nav-btn-active" if current == target else "nav-btn"
        if cols[i].button(label, key=f"menu_{target}", use_container_width=True):
            navigate_to(target)

        cols[i].markdown(f"<style>div[data-testid='stButton'] button {{ class: {classe}; }}</style>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------
# DASHBOARD PRINCIPAL
# ---------------------------------------------------
def show_page(navigate_to):

    # Renderiza o menu superior
    top_menu(navigate_to)

    # ====== ESTILO GLOBAL ======
    st.markdown("""
        <style>
            .block-container {
                padding-top: 1rem !important;
            }

            .glass-card {
                background: rgba(255, 255, 255, 0.08);
                backdrop-filter: blur(12px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                padding: 22px;
                border-radius: 14px;
                box-shadow: 0px 8px 20px rgba(0,0,0,0.25);
            }

            .title-main {
                font-size: 2.4rem;
                font-weight: 700;
                color: #fff;
                margin-bottom: 10px;
            }

            .section-title {
                font-size: 1.5rem;
                font-weight: 600;
                margin-bottom: 10px;
                color: #e0e0e0;
            }

            .metric-box {
                background: rgba(255,255,255,0.05);
                border: 1px solid rgba(255,255,255,0.1);
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 12px;
            }
        </style>
    """, unsafe_allow_html=True)

    # ===== TÍTULO =====
    st.markdown("<div class='title-main'>Painel de Controle Principal</div>", unsafe_allow_html=True)

    # ===== LAYOUT PRINCIPAL =====
    col_left, col_right = st.columns([1, 1.6], gap="large")

    with col_left:

        st.markdown(f"""
            <div class="glass-card">
                <h3 style="color:white; margin-bottom:5px;">Olá, {st.session_state.get('user', 'Visitante')} 👋</h3>
                <p style="color:#ccc;">📍 Fazenda Ativa: <strong>Canudos - Bahia</strong></p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("<div class='section-title'>Resumo da Propriedade</div>", unsafe_allow_html=True)

        st.markdown("""
            <div class="metric-box">
                <div style="color:#ccc;">Status do Solo</div>
                <div style="color:white; font-size:1.4rem; font-weight:700;">Normal</div>
                <div style="color:#82e0a8;">pH 6.8</div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("""
            <div class="metric-box">
                <div style="color:#ccc;">Risco Hídrico (30 dias)</div>
                <div style="color:white; font-size:1.4rem; font-weight:700;">Baixo</div>
                <div style="color:#e57373;">-5% anomalia</div>
            </div>
        """, unsafe_allow_html=True)

        st.info("Use o menu superior para navegar no sistema.")

    with col_right:

        st.markdown("<div class='section-title'>Localização da Propriedade</div>", unsafe_allow_html=True)

        df_map = pd.DataFrame({'lat': [-9.934], 'lon': [-38.97]})
        st.map(df_map, zoom=11, use_container_width=True)

        st.caption("Visão geral da localização da fazenda registrada.")
