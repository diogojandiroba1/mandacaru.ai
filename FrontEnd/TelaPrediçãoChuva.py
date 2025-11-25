import streamlit as st
import pickle
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import timedelta
import os

# ============================================================
# FUNÇÕES DE CARREGAMENTO
# ============================================================

@st.cache_resource
def carregar_modelo_ndvi():
    model_path = os.path.join(os.path.dirname(__file__), '..', 'Modelos', 'modelo_ndvi_compat.pkl')
    try:
        with open(model_path, 'rb') as file:
            obj = pickle.load(file)  # {"model": ..., "features": ...}
        return obj
    except Exception as e:
        st.error(f"Erro ao carregar modelo NDVI: {e}")
        return None


@st.cache_data
def carregar_dados():
    data_path = os.path.join(os.path.dirname(__file__), '..', 'Dados', 'dataCanudos.csv')
    try:
        df = pd.read_csv(data_path)
        df["data"] = pd.to_datetime(df["data"].astype(str), format="%Y%m%d")
        return df.sort_values("data").reset_index(drop=True)
    except:
        return None


# ============================================================
# PREVISÃO SIMPLES DO CLIMA
# ============================================================

def prever_clima_historico(df_hist, datas_futuras, anos_base=5):
    preds = []
    data_max = df_hist['data'].max()
    data_inicio = data_max - timedelta(days=anos_base * 365)

    df_base = df_hist[df_hist['data'] >= data_inicio]
    if df_base.empty:
        df_base = df_hist

    medias = df_base.groupby(df_base["data"].dt.month)[["precipitacao", "evapotranspiracao", "umidade_relativa"]].mean()

    for d in datas_futuras:
        m = d.month
        if m in medias.index:
            preds.append({
                "data": d,
                "precipitacao": medias.loc[m, "precipitacao"],
                "evapotranspiracao": medias.loc[m, "evapotranspiracao"],
                "umidade_relativa": medias.loc[m, "umidade_relativa"]
            })

    return pd.DataFrame(preds)


# ============================================================
# GERAR FUTURO IDEAL COMPATÍVEL COM O MODELO
# ============================================================

def gerar_futuro_ideal(df_hist, modelo, features_modelo, dias=30):

    last_date = df_hist["data"].max()
    datas_futuras = [last_date + timedelta(days=i) for i in range(1, dias+1)]

    # previsões climáticas simples
    df_clima = prever_clima_historico(df_hist, datas_futuras)

    if df_clima.empty:
        return pd.DataFrame()

    # copiar dados fixos: solo, topo, etc
    last_row = df_hist.iloc[-1]
    for col in ["argila", "areia", "altitude", "ph_solo", "carbono_organico", "radiacao_solar", "vento"]:
        df_clima[col] = last_row[col]

    # sazonalidade
    df_clima["dia_ano"] = df_clima["data"].dt.dayofyear
    df_clima["dia_sin"] = np.sin(2 * np.pi * df_clima["dia_ano"] / 365)
    df_clima["dia_cos"] = np.cos(2 * np.pi * df_clima["dia_ano"] / 365)

    # acumulados futuros (clima previsto)
    df_clima["chuva_acum_30d"] = df_clima["precipitacao"].rolling(30, min_periods=1).sum()
    df_clima["evapo_acum_30d"] = df_clima["evapotranspiracao"].rolling(30, min_periods=1).sum()
    df_clima["balanco_30d"] = df_clima["chuva_acum_30d"] - df_clima["evapo_acum_30d"]

    df_clima = df_clima.fillna(method="bfill").fillna(method="ffill")

    df_clima["ndvi_ideal"] = modelo.predict(df_clima[features_modelo])

    return df_clima


# ============================================================
# DIAGNÓSTICO AGRONÔMICO
# ============================================================

def gerar_diagnostico_avancado(gap, chuva, anom):

    # 🌧 pouca chuva e anomalia muito negativa
    if anom < -0.10 and chuva < 30:
        return """
        <h4 style='color:#D32F2F'>🚨 Risco Alto – Colapso Fisiológico</h4>
        <p>A lavoura apresenta sinais claros de estresse severo. O NDVI está muito abaixo do ideal e a baixa previsão de chuvas agrava a situação.</p>
        <ul>
            <li>Déficit hídrico crítico afetando fotossíntese.</li>
            <li>Redução do crescimento vegetativo nas próximas 48h.</li>
            <li>Risco elevado de queda de folhas e abortamento floral.</li>
        </ul>
        <b>Ação recomendada:</b> irrigação de emergência + adubação foliar antisstressante (aminoácidos e K).
        """

    # 🌧 chuva chegando mas planta sofrendo
    elif anom < -0.10:
        return """
        <h4 style='color:#FF9800'>🌦 Recuperação Provável</h4>
        <p>A vegetação apresenta estresse moderado a severo, mas há chuva prevista, o que deve ajudar na recuperação do vigor vegetal.</p>
        <ul>
            <li>Sistema radicular ativo, porém limitado pelo déficit hídrico recente.</li>
            <li>NDVI deve subir gradualmente após a regularização da umidade.</li>
            <li>Solo com tendência à compactação superficial.</li>
        </ul>
        <b>Ação recomendada:</b> aguardar chuva, depois aplicar bioestimulante para retomada do crescimento.
        """

    # 🌱 alto potencial + chuva suficiente
    elif gap > 0.05 and chuva >= 30:
        return """
        <h4 style='color:#388E3C'>🚀 Janela de Alta Produtividade</h4>
        <p>A lavoura demonstra alto potencial produtivo e o clima está favorável, oferecendo condições ideais para desenvolvimento vegetativo.</p>
        <ul>
            <li>Expectativa de forte incremento no NDVI nos próximos dias.</li>
            <li>Alta disponibilidade hídrica e boa radiação solar.</li>
            <li>Momento ideal para estratégias de adubação nitrogenada.</li>
        </ul>
        <b>Ação recomendada:</b> aplicar adubação de cobertura e monitorar doenças devido à umidade.
        """

    # 🌱 alto potencial mas chuva baixa
    elif gap > 0.05:
        return """
        <h4 style='color:#FBC02D'>⚠ Potencial Ameaçado</h4>
        <p>A planta possui bom potencial fotossintético, mas a limitação hídrica pode reduzir o crescimento esperado para os próximos dias.</p>
        <ul>
            <li>NDVI deve estabilizar ou cair caso o solo não receba reposição hídrica.</li>
            <li>Risco de estresse nutricional leve.</li>
            <li>Redução da eficiência metabólica por falta de água.</li>
        </ul>
        <b>Ação recomendada:</b> irrigação complementar leve para manter o vigor e evitar perda de produtividade.
        """

    # 🍂 maturação natural do ciclo
    elif gap < -0.05:
        return """
        <h4 style='color:#757575'>🍂 Maturação do Ciclo</h4>
        <p>A diminuição do NDVI é compatível com o período de maturação. A planta está concluindo seu ciclo fisiológico.</p>
        <ul>
            <li>Redução natural do índice de vegetação.</li>
            <li>Redistribuição de nutrientes para grãos/frutos.</li>
            <li>Baixa resposta a intervenções neste estágio.</li>
        </ul>
        <b>Ação recomendada:</b> suspender insumos e direcionar foco para planejamento de colheita.
        """

    # 🙂 dentro do normal
    else:
        return """
        <h4 style='color:#0288D1'>✅ Estável – Dentro do Esperado</h4>
        <p>A lavoura apresenta comportamento normal para a época do ano. O NDVI está alinhado com a média histórica e não há sinais de estresse relevante.</p>
        <ul>
            <li>Transpiração e fotossíntese em níveis adequados.</li>
            <li>Risco hídrico baixo.</li>
            <li>Clima favorecendo estabilidade do dossel.</li>
        </ul>
        <b>Ação recomendada:</b> manter o manejo atual e monitorar meteorologia normalmente.
        """



# ============================================================
# INTERFACE PRINCIPAL
# ============================================================

def show_page():
    st.title("Diagnóstico de NDVI com IA")

    obj = carregar_modelo_ndvi()
    if obj is None:
        return

    model = obj["model"]
    features_modelo = obj["features"]

    df = carregar_dados()
    if df is None:
        st.error("Erro carregando dados.")
        return

    df_calc = df.copy()

    # acumulados reais
    df_calc["chuva_acum_30d"] = df_calc["precipitacao"].rolling(30).sum()
    df_calc["evapo_acum_30d"] = df_calc["evapotranspiracao"].rolling(30).sum()
    df_calc["balanco_30d"] = df_calc["chuva_acum_30d"] - df_calc["evapo_acum_30d"]

    df_calc["dia_ano"] = df_calc["data"].dt.dayofyear
    df_calc["dia_sin"] = np.sin(2 * np.pi * df_calc["dia_ano"] / 365)
    df_calc["dia_cos"] = np.cos(2 * np.pi * df_calc["dia_ano"] / 365)

    df_calc = df_calc.dropna().reset_index(drop=True)

    df_fut = gerar_futuro_ideal(df_calc, model, features_modelo, dias=30)

    if df_fut.empty:
        st.warning("Falha ao gerar previsão futura.")
        return

    # DIAGNÓSTICO AGRONÔMICO
    col1, col2 = st.columns([1, 2])

    with col1:
        ultimo_real = df_calc.iloc[-1]["ndvi"]
        ndvi_prev_atual = model.predict(pd.DataFrame([df_calc.iloc[-1][features_modelo]]))[0]
        anomalia = ultimo_real - ndvi_prev_atual

        ultimo_ideal = df_fut.iloc[-1]["ndvi_ideal"]
        gap = ultimo_ideal - ultimo_real
        chuva_prev = df_fut["precipitacao"].sum()

        st.markdown("### 🧠 Diagnóstico")
        st.markdown(gerar_diagnostico_avancado(gap, chuva_prev, anomalia), unsafe_allow_html=True)

    # GRÁFICO
    with col2:
        st.markdown("### 📈 NDVI Real vs Ideal")

        df_hist = df_calc.tail(180)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_hist["data"], y=df_hist["ndvi"],
            mode="lines", name="NDVI Real"
        ))

        fig.add_trace(go.Scatter(
            x=df_fut["data"], y=df_fut["ndvi_ideal"],
            mode="lines", name="NDVI Ideal", line=dict(dash="dash")
        ))

        st.plotly_chart(fig, use_container_width=True)


# EXECUÇÃO LOCAL
if __name__ == "__main__":
    st.set_page_config(page_title="Predição NDVI", layout="wide")
    show_page()
