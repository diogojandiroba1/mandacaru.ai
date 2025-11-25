import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import os

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "Dados", "propriedades.csv")

geolocator = Nominatim(user_agent="mandacaru_ai_app")


def salvar_propriedade(dados):
    df_new = pd.DataFrame([dados])

    # Se não existir o arquivo, cria com as colunas certas
    if not os.path.exists(CSV_PATH):
        df_new.to_csv(CSV_PATH, index=False)
        return

    # Carrega removendo colunas antigas indesejadas (area, cultura)
    df_old = pd.read_csv(CSV_PATH)
    colunas_validas = ["estado", "cidade", "latitude", "longitude"]
    df_old = df_old[colunas_validas]

    df_final = pd.concat([df_old, df_new], ignore_index=True)
    df_final.to_csv(CSV_PATH, index=False)


def detectar_cidade(lat, lon):
    """Detecta cidade/estado automaticamente via geolocalização reversa."""
    try:
        location = geolocator.reverse((lat, lon), language="pt")
        if not location:
            return None, None

        address = location.raw.get("address", {})

        cidade = address.get("town") or address.get("city") or address.get("village")
        estado = address.get("state")
        return cidade, estado
    except:
        return None, None


def show_page():

    st.markdown(
        """
        <h1 style='font-size: 2.4rem;'>🏡 Propriedades Registradas</h1>
        <p style='opacity:0.7;'>Gerencie e cadastre novas fazendas no sistema.</p>
        """,
        unsafe_allow_html=True
    )

    # ================================
    #   LISTA DE PROPRIEDADES
    # ================================
    st.markdown("### 📋 Propriedades Cadastradas")

    if os.path.exists(CSV_PATH):
        df_props = pd.read_csv(CSV_PATH)

        # Remove colunas antigas caso ainda existam no arquivo
        colunas_validas = ["estado", "cidade", "latitude", "longitude"]
        df_props = df_props[colunas_validas]

        if df_props.empty:
            st.warning("Nenhuma propriedade cadastrada ainda.")
        else:
            st.dataframe(
                df_props.style.set_properties(**{
                    "background-color": "#111",
                    "color": "white",
                    "border-color": "#444"
                }),
                use_container_width=True
            )

            # -------- Mapa geral --------
            st.markdown("### 🌍 Visualização no Mapa")

            mapa_props = folium.Map(location=[-10.5, -37.1], zoom_start=6)

            for _, row in df_props.iterrows():
                folium.Marker(
                    [row["latitude"], row["longitude"]],
                    popup=f"{row['cidade']} - {row['estado']}"
                ).add_to(mapa_props)

            st_folium(mapa_props, height=450, use_container_width=True)

    else:
        st.info("Nenhuma propriedade cadastrada ainda.")

    st.write("---")

    # ================================
    #   CADASTRAR NOVA PROPRIEDADE
    # ================================
    st.markdown("## ➕ Cadastrar Nova Propriedade")
    st.write("Selecione no mapa o local da fazenda.")

    mapa = folium.Map(location=[-10.5, -37.1], zoom_start=6)

    if "marker" in st.session_state:
        folium.Marker(st.session_state.marker).add_to(mapa)

    map_data = st_folium(mapa, height=450, use_container_width=True)

    # Coleta da posição clicada
    if map_data and map_data.get("last_clicked"):
        lat = map_data["last_clicked"]["lat"]
        lon = map_data["last_clicked"]["lng"]
        st.session_state.marker = (lat, lon)

        cidade_auto, estado_auto = detectar_cidade(lat, lon)
        st.session_state.cidade_auto = cidade_auto
        st.session_state.estado_auto = estado_auto

        st.success(f"Local selecionado: LAT {lat:.6f}, LON {lon:.6f}")

    st.write("---")
    st.subheader("Informações da Propriedade")

    # Mostrar campos automáticos
    col1, col2 = st.columns(2)
    lat_val, lon_val = None, None
    if "marker" in st.session_state:
        lat_val, lon_val = st.session_state.marker

    with col1:
        st.text_input("Latitude", value=f"{lat_val:.6f}" if lat_val else "", disabled=True)
    with col2:
        st.text_input("Longitude", value=f"{lon_val:.6f}" if lon_val else "", disabled=True)

    # Formulário
    with st.form("form_prop"):

        estado_form = st.text_input(
            "Estado",
            value=st.session_state.get("estado_auto", "") or ""
        )

        cidade_form = st.text_input(
            "Cidade",
            value=st.session_state.get("cidade_auto", "") or ""
        )

        botao = st.form_submit_button("Salvar Propriedade")

    # SALVAR
    if botao:
        if "marker" not in st.session_state:
            st.error("Selecione um ponto no mapa antes de salvar.")
            return

        lat, lon = st.session_state.marker

        dados = {
            "estado": estado_form,
            "cidade": cidade_form,
            "latitude": lat,
            "longitude": lon,
        }

        salvar_propriedade(dados)

        st.success("Propriedade cadastrada com sucesso!")
        st.info("Arquivo salvo em: Dados/propriedades.csv")

        st.experimental_rerun()


if __name__ == "__main__":
    st.set_page_config(page_title="Cadastro Propriedade", layout="wide")
    show_page()
