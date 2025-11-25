import streamlit as st
import pandas as pd
import pickle
import os
import numpy as np

# =======================================================================
# CARREGAR MODELO
# =======================================================================

@st.cache_resource
def carregar_modelo():
    model_path = os.path.join(os.path.dirname(__file__), '..', 'Modelos', 'modelo_ndvi_compat.pkl')
    try:
        with open(model_path, "rb") as f:
            obj = pickle.load(f)
        if not isinstance(obj, dict) or "model" not in obj or "features" not in obj:
            st.error("Modelo inválido. Esperado formato {model, features}.")
            return None
        return obj
    except Exception as e:
        st.error(f"Erro ao carregar modelo: {e}")
        return None


# =======================================================================
# CARREGAR CSV
# =======================================================================

@st.cache_data
def carregar_dados():
    data_path = os.path.join(os.path.dirname(__file__), '..', 'Dados', 'dataCanudos.csv')
    try:
        df = pd.read_csv(data_path)
        df["data"] = pd.to_datetime(df["data"].astype(str), format="%Y%m%d")
        return df.sort_values("data").reset_index(drop=True)
    except:
        return None


# =======================================================================
# INSIGHTS DETALHADOS
# =======================================================================

def gerar_insights_solo(pred, row):
    ndvi = row["ndvi"]
    chuva = row["precipitacao"]
    umid = row["umidade_relativa"]
    temp = row["temp_media"]
    vento = row["vento"]

    insights = []

    if pred >= 0.5:
        insights.append("O modelo indica solo saudável, com boa reação às condições climáticas recentes.")
    else:
        insights.append("O solo apresenta risco moderado a alto, sugerindo redução no vigor vegetativo.")

    if ndvi < 0.35:
        insights.append(f"NDVI {ndvi:.2f}: muito baixo, típico de forte estresse hídrico ou estágio inicial.")
    elif ndvi < 0.5:
        insights.append(f"NDVI {ndvi:.2f}: moderado, indicando desenvolvimento limitado.")
    else:
        insights.append(f"NDVI {ndvi:.2f}: bom vigor vegetativo.")

    if chuva < 2:
        insights.append(f"Chuva extremamente baixa ({chuva:.1f} mm), risco de estresse hídrico.")
    elif chuva < 10:
        insights.append(f"Chuva moderada ({chuva:.1f} mm), ajuda, mas ainda insuficiente.")
    else:
        insights.append(f"Boa chuva ({chuva:.1f} mm), favorecendo recuperação do solo.")

    if umid < 40:
        insights.append("Umidade relativa muito baixa, aumentando evapotranspiração.")
    elif umid < 55:
        insights.append("Umidade moderada, podendo gerar leve estresse hídrico.")
    else:
        insights.append("Umidade adequada, ideal para o crescimento vegetativo.")

    if temp > 30:
        insights.append(f"Temperatura elevada ({temp:.1f}°C), aumentando demanda hídrica.")
    elif temp < 18:
        insights.append(f"Temperatura baixa ({temp:.1f}°C), reduzindo o ritmo de desenvolvimento.")
    else:
        insights.append(f"Temperatura ideal ({temp:.1f}°C).")

    if vento > 8:
        insights.append("Ventos fortes, aumentando desidratação foliar.")
    elif vento < 3:
        insights.append("Ventos fracos, microclima estável e favorável.")
    else:
        insights.append("Ventos moderados, sem impacto significativo.")

    return insights



# =======================================================================
# INTERFACE PRINCIPAL
# =======================================================================

def show_page():

    # ============================ ESTILO GLOBAL ===============================
    st.markdown("""
        <style>
            .centered {
                max-width: 950px;
                margin-left: auto;
                margin-right: auto;
            }
            .section-title {
                color: #FFFFFF;
                font-size: 26px;
                margin-top: 40px;
                font-weight: 600;
                border-left: 4px solid #4FC3F7;
                padding-left: 10px;
            }
            .divider {
                height: 1px;
                background: rgba(255,255,255,0.08);
                margin: 25px 0;
            }
            .metric-card {
                background: #1A1D23;
                padding: 18px;
                border-radius: 10px;
                border: 1px solid rgba(255,255,255,0.05);
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align:center; color:white;'>Diagnóstico Inteligente do Solo</h1>", unsafe_allow_html=True)

    df = carregar_dados()
    modelo_obj = carregar_modelo()

    if df is None or modelo_obj is None:
        st.error("Erro ao carregar dados ou modelo.")
        return

    # Criar features derivadas
    df["chuva_acum_30d"] = df["precipitacao"].rolling(30).sum()
    df["evapo_acum_30d"] = df["evapotranspiracao"].rolling(30).sum()
    df["balanco_30d"] = df["chuva_acum_30d"] - df["evapo_acum_30d"]

    df["dia_ano"] = df["data"].dt.dayofyear
    df["dia_sin"] = np.sin(2*np.pi*df["dia_ano"]/365)
    df["dia_cos"] = np.cos(2*np.pi*df["dia_ano"]/365)

    df = df.dropna().reset_index(drop=True)

    # =======================================================================
    # SEÇÃO 1 – SELEÇÃO DE DATA
    # =======================================================================

    st.markdown("<div class='centered'>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>📅 Seleção da Data</div>", unsafe_allow_html=True)

    data_selecionada = st.date_input(
        "",
        value=df["data"].max().date(),
        min_value=df["data"].min().date(),
        max_value=df["data"].max().date(),
    )

    gerar = st.button("Gerar Diagnóstico")

    if not gerar:
        st.info("Selecione uma data e clique em gerar.")
        st.markdown("</div>", unsafe_allow_html=True)
        return


    # Selecionar linha do dado
    linha = df[df["data"].dt.date == data_selecionada]
    if linha.empty:
        st.warning("Nenhum dado encontrado.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    row = linha.iloc[0]

    # Modelo
    model = modelo_obj["model"]
    features = modelo_obj["features"]
    input_data = pd.DataFrame([row[features].values], columns=features)
    pred = model.predict(input_data)[0]

    status = "Solo saudável" if pred >= 0.5 else "Solo sob risco"
    cor = "#4CAF50" if pred >= 0.5 else "#FFA726"

    # =======================================================================
    # SEÇÃO 2 – RESULTADO
    # =======================================================================

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🌡️ Resultado do Diagnóstico</div>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="
            background:{cor};
            padding:22px;
            border-radius:12px;
            text-align:center;
            color:white;
            font-size:24px;
            font-weight:bold;">
            {status.upper()}<br>
            <span style='font-size:16px;'>Score: {pred:.3f}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # =======================================================================
    # SEÇÃO 3 – DADOS DO DIA
    # =======================================================================

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🗂️ Dados do Dia</div>", unsafe_allow_html=True)

    fazenda = row.get("id_fazenda", "Não informado")
    st.markdown(f"### 🌱 Propriedade analisada: **{fazenda}**")

    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)

    with col1: st.markdown("##### 📅 Data"); st.write(row['data'].strftime('%d/%m/%Y'))
    with col2: st.markdown("##### 🌡️ Temperatura"); st.write(f"{row['temp_media']} °C")
    with col3: st.markdown("##### 🌧️ Chuva"); st.write(f"{row['precipitacao']} mm")
    with col4: st.markdown("##### 💧 Umidade"); st.write(f"{row['umidade_relativa']} %")
    with col5: st.markdown("##### 🌿 NDVI"); st.write(f"{row['ndvi']:.3f}")
    with col6: st.markdown("##### 🧪 pH do solo"); st.write(f"{row['ph_solo']:.2f}")

    # =======================================================================
    # SEÇÃO 4 – INSIGHTS
    # =======================================================================

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>📊 Análise Detalhada</div>", unsafe_allow_html=True)

    insights = gerar_insights_solo(pred, row)

    for texto in insights:
        st.markdown(
            f"""
            <div class='insight-card' style='border-color:{cor};'>
                {texto}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # ==============================
    # RODAPÉ FIXO (sempre visível)
    # ==============================
    st.markdown("""
        <style>
            .footer-fixed {
                position: fixed;
                left: 0;
                bottom: 0;
                width: 100%;
                background-color: #E8D8B5; /* bege suave */
                color: black;
                text-align: center;
                padding: 10px 0;
                font-size: 14px;
                font-weight: 600;
                z-index: 9999;
                border-top: 1px solid rgba(0,0,0,0.15);
            }
        </style>

        <div class="footer-fixed">
            MANDACARU.AI | CONTATOS 79 (XXXX-XXXX)
        </div>
    """, unsafe_allow_html=True)

# Execução local
if __name__ == "__main__":
    st.set_page_config(page_title="Diagnóstico do Solo", layout="wide")
    show_page()
