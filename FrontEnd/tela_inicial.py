import streamlit as st
import base64

# ----------------------------------------------------------
# Função utilitária para converter imagens locais em base64
# ----------------------------------------------------------
def img_to_base64(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


# ----------------------------------------------------------
# Página inicial da plataforma
# ----------------------------------------------------------
def show_page(navigate_to):

    # Convertendo as imagens da pasta Fotos
    img1 = img_to_base64("/home/aluno/Documentos/Mandacaru.AI/Fotos/10598565.jpg")
    img2 = img_to_base64("/home/aluno/Documentos/Mandacaru.AI/Fotos/como-o-semiarido-brasileiro-se-transformou-em-polo-produtivo-de-fruticultura-plantacao-de-manga-em-petrolina-01-1140x641-1.jpeg")
    img3 = img_to_base64("/home/aluno/Documentos/Mandacaru.AI/Fotos/Irrigacao-agricultura-irrigada.jpeg")

    # ------------------------------------------------------
    # Estilos CSS
    # ------------------------------------------------------
    st.markdown("""
        <style>
            .block-container {
                padding: 0 !important;
                margin: 0 !important;
                max-width: 100% !important;
            }
            .hero-section {
                text-align: center;
                padding: 70px 20px;
                background: linear-gradient(135deg, #8BC34A, #558B2F);
                color: white;
            }
            .hero-section h1 {
                font-size: 3.4em;
                font-weight: 800;
                margin-bottom: 0.2em;
            }
            .hero-section h2 {
                font-size: 1.4em;
                font-weight: 300;
                opacity: 0.9;
            }
                
            .stButton > button {
            background-color: #4CAF50 !important;   /* Verde */
            color: white !important;
            border-radius: 8px !important;
            padding: 10px 20px !important;
            border: none !important;
            font-size: 1.1em !important;
            font-weight: 600 !important;
            cursor: pointer;
            }
            .stButton > button:hover {
            background-color: #45a049 !important;   /* Verde mais escuro ao passar o mouse */
            }
    
            .benefits-section {
                padding: 50px 20px;
                background-color: #f4f7f4;
                text-align: center;
            }
            .benefits-section h3 {
                font-size: 2.2em;
                margin-bottom: 40px;
                font-weight: 700;
                color: #333;
            }
            .card {
                background-color: white;
                border-radius: 18px;
                overflow: hidden;
                box-shadow: 0 6px 18px rgba(0,0,0,0.1);
                transition: transform 0.25s;
                height: 100%;
                display: flex;
                flex-direction: column;
            }
            .card:hover {
                transform: translateY(-8px);
            }
            .card-image {
                height: 180px;
                width: 100%;
                object-fit: cover;
            }
            .card-content {
                padding: 20px;
                flex-grow: 1;
            }
            .card-content h4 {
                font-size: 1.3em;
                margin-bottom: 10px;
                color: #558B2F;
                font-weight: 700;
            }
            .card-content p {
                font-size: 1em;
                color: #555;
                line-height: 1.5;
            }
            .final-cta-section {
                text-align: center;
                padding: 60px 20px;
            }
            .final-cta-section h3 {
                font-size: 2.2em;
                font-weight: 700;
            }
            .final-cta-section p {
                font-size: 1.1em;
                max-width: 600px;
                color: #555;
                margin: auto;
            }
            .landing-btn {
                font-size: 1.2em;
                padding: 12px 25px;
                background-color: #689F38;
                color: white;
                border-radius: 8px;
                border: none;
                cursor: pointer;
                width: 100%;
            }
            .landing-btn:hover {
                background-color: #558B2F;
            }
        </style>
    """, unsafe_allow_html=True)

    # ----------------------------------------------------------
    # HERO SECTION
    # ----------------------------------------------------------
    st.markdown("""
        <div class="hero-section">
            <h1>Mandacaru.AI 🌵</h1>
            <h2>Inteligência climática e solo vivo para o semiárido.</h2>
        </div>
    """, unsafe_allow_html=True)

    # ----------------------------------------------------------
    # BENEFÍCIOS
    # ----------------------------------------------------------
    st.markdown("""
        <div class="benefits-section">
            <h3>A tecnologia que fala a língua do campo</h3>
        </div>
    """, unsafe_allow_html=True)

    # ----------------------------------------------------------
    # CARDS COM IMAGENS REAIS
    # ----------------------------------------------------------
    _, box, _ = st.columns([1, 10, 1])

    with box:
        col1, col2, col3 = st.columns(3, gap="large")

        # CARD 1
        with col1:
            st.markdown(f"""
                <div class="card">
                    <img src="data:image/jpeg;base64,{img1}" class="card-image">
                    <div class="card-content">
                        <h4>Diagnóstico Preciso</h4>
                        <p>Analise a saúde do solo com indicadores inteligentes e recomendações práticas.</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        # CARD 2
        with col2:
            st.markdown(f"""
                <div class="card">
                    <img src="data:image/jpeg;base64,{img2}" class="card-image">
                    <div class="card-content">
                        <h4>Previsão Inteligente</h4>
                        <p>Antecipe riscos com modelos climáticos e NDVI treinados para o semiárido.</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        # CARD 3
        with col3:
            st.markdown(f"""
                <div class="card">
                    <img src="data:image/jpeg;base64,{img3}" class="card-image">
                    <div class="card-content">
                        <h4>Decisões Rentáveis</h4>
                        <p>Use dados reais para reduzir custos, evitar perdas e aumentar sua produtividade.</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    # ----------------------------------------------------------
    # CTA FINAL
    # ----------------------------------------------------------
    st.markdown("""
        <div class="final-cta-section">
            <h3>Preveja. Planeje. Produza com segurança.</h3>
            <p>Transforme sua fazenda usando ciência, dados e inteligência artificial.</p>
        </div>
    """, unsafe_allow_html=True)

    # ----------------------------------------------------------
    # BOTÃO DE ACESSO
    # ----------------------------------------------------------
    _, col_btn, _ = st.columns([2, 1, 2])

    with col_btn:
        if st.button("Acessar a Plataforma", use_container_width=True, key="go_plat"):
            navigate_to("login")

