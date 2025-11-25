import streamlit as st

# ============================================================
# CONFIGURAÇÃO DA PÁGINA (DEVE SER A PRIMEIRA LINHA)
# ============================================================
st.set_page_config(
    page_title="Mandacaru.AI",
    page_icon="🌵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# IMPORTAÇÃO DAS TELAS
# ============================================================
import tela_inicial
import tela_login
import tela_dashboard
import tela_clima
import tela_propriedade

# Telas de Machine Learning
try:
    from telaDiagnostico import show_page as show_diagnostico_page
    from TelaPrediçãoChuva import show_page as show_predicao_page
    ML_PAGES_LOADED = True
except ImportError:
    ML_PAGES_LOADED = False

# ============================================================
# ESTADO GLOBAL
# ============================================================
if "page" not in st.session_state:
    st.session_state.page = "landing"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = "Visitante"


# ============================================================
# FUNÇÃO DE NAVEGAÇÃO
# ============================================================
def navigate_to(page):
    st.session_state.page = page
    st.rerun()


# ============================================================
# CSS GLOBAL + FOOTER FIXO (AQUI ESTÁ A SOLUÇÃO)
# ============================================================
def setup_global_styles():
    st.markdown(
        """
        <style>
            :root { 
                --primary: #8BC34A; 
                --dark: #689F38; 
            }

            /* Remove menus padrão */
            header, footer, #MainMenu {visibility: hidden;}

            /* Aumenta espaço inferior para não cobrir conteúdo */
            .block-container {
                padding-bottom: 80px !important;
            }

            /* -------- FOOTER FIXO GLOBAL -------- */
            .footer-fixed {
                position: fixed;
                bottom: 0;
                left: 0;
                width: 100%;
                background-color: #EFEBE9; /* bege */
                color: #5D4037;
                text-align: center;
                padding: 10px 0;
                font-size: 13px;
                border-top: 1px solid #D7CCC8;
                z-index: 9999;
            }

            /* -------- HEADER -------- */
            .custom-header {
                background-color: var(--primary);
                padding: 12px 20px;
                border-bottom: 4px solid var(--dark);
                margin-bottom: 25px;
            }
            .nav-title {
                color: white;
                font-size: 26px;
                font-weight: bold;
            }

            /* Botões navbar */
            .stButton button {
                background-color: var(--primary);
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                padding: 8px 15px;
            }
            .stButton button:hover {
                background-color: var(--dark);
                color: white;
            }

            /* Botão Sair */
            button[kind="secondary"] {
                background-color: #ff4b4b !important;
                color: white !important;
                border: none !important;
            }
            button[kind="secondary"]:hover {
                background-color: #a30000 !important;
            }
        </style>

        <!-- FOOTER SEMPRE RENDERIZADO -->
        <div class="footer-fixed">
            MANDACARU.AI | CONTATOS 79 (XXXX-XXXX)
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# HEADER SUPERIOR
# ============================================================
def render_header():
    st.markdown('<div class="custom-header">', unsafe_allow_html=True)

    col_title, col_nav = st.columns([1, 3])

    with col_title:
        st.markdown('<span class="nav-title">Mandacaru.AI 🌵</span>', unsafe_allow_html=True)

    with col_nav:
        c1, c2, c3, c4, c5 = st.columns(5)

        with c1:
            if st.button("Dashboard"):
                navigate_to("dashboard")

        with c2:
            if st.button("Diagnóstico"):
                navigate_to("diagnostico")

        with c3:
            if st.button("Predição"):
                navigate_to("predicao")

        with c4:
            if st.button("Propriedade"):
                navigate_to("propriedade")

        with c5:
            if st.button("Sair", type="secondary"):
                st.session_state.logged_in = False
                navigate_to("landing")

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# ROTEAMENTO PRINCIPAL
# ============================================================
def main():

    # Carrega CSS e footer global apenas uma vez
    if "styles_loaded" not in st.session_state:
        setup_global_styles()
        st.session_state.styles_loaded = True

    # Exibe header se não for página inicial
    if st.session_state.page != "landing" and st.session_state.logged_in:
        render_header()

    # Roteamento
    page = st.session_state.page
    logged = st.session_state.logged_in

    if page == "landing":
        tela_inicial.show_page(navigate_to)
    elif page == "login":
        tela_login.show_page(navigate_to)
    elif not logged:
        navigate_to("login")
    elif page == "dashboard":
        tela_dashboard.show_page(navigate_to)
    elif page == "clima":
        tela_clima.show_page()
    elif page == "propriedade":
        tela_propriedade.show_page()
    elif page == "diagnostico":
        if ML_PAGES_LOADED:
            show_diagnostico_page()
        else:
            st.error("Módulo de diagnóstico não encontrado.")
    elif page == "predicao":
        if ML_PAGES_LOADED:
            show_predicao_page()
        else:
            st.error("Módulo de predição não encontrado.")


# ============================================================
if __name__ == "__main__":
    main()
