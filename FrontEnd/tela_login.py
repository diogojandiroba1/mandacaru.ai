import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000"

def show_page(navigate_to):
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h2 style='text-align: center;'>Bem vindo a revolução! 🌵</h2>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Entrar", "Cadastrar"])
        
        with tab1:
            with st.form("login_form"):
                email = st.text_input("Email", placeholder="seuemail@exemplo.com")
                senha = st.text_input("Senha", type="password")
                
                if st.form_submit_button("Acessar Conta", use_container_width=True):
                    if not email or not senha:
                        st.error("Por favor, insira email e senha.")
                        return
                    
                    try:
                        response = requests.post(f"{BACKEND_URL}/login", json={
                            "email": email,
                            "password": senha
                        })
                        
                        if response.status_code == 200:
                            st.session_state.logged_in = True
                            st.session_state.user = response.json().get("user", email.split('@')[0])
                            st.success("Login realizado com sucesso!")
                            navigate_to('dashboard')
                        else:
                            try:
                                error_detail = response.json().get("detail", "Credenciais inválidas")
                            except:
                                error_detail = response.text # Fallback to raw text if not JSON
                            st.error(f"Erro no login: {error_detail}")
                    except requests.exceptions.ConnectionError:
                        st.error("Não foi possível conectar ao servidor. Verifique se o backend está rodando.")
                    except Exception as e:
                        st.error(f"Ocorreu um erro inesperado: {e}")
        
        with tab2:
            with st.form("cadastro_form"):
                nome = st.text_input("Nome Completo")
                email_cad = st.text_input("Email")
                cpf = st.text_input("CPF", placeholder="000.000.000-00")
                senha_cad = st.text_input("Criar Senha", type="password")
                
                if st.form_submit_button("Cadastrar-se", use_container_width=True):
                    if not email_cad or not senha_cad:
                        st.error("Email e senha são obrigatórios para cadastro.")
                        return
                    
                    try:
                        response = requests.post(f"{BACKEND_URL}/register", json={
                            "email": email_cad,
                            "password": senha_cad
                        })
                        
                        if response.status_code == 201:
                            st.success("Cadastro realizado com sucesso! Faça login na aba ao lado.")
                        else:
                            try:
                                error_detail = response.json().get("detail", "Erro desconhecido")
                            except:
                                error_detail = response.text # Fallback to raw text if not JSON
                            st.error(f"Erro ao cadastrar: {error_detail}")
                    except requests.exceptions.ConnectionError:
                        st.error("Não foi possível conectar ao servidor. Verifique se o backend está rodando.")
                    except Exception as e:
                        st.error(f"Ocorreu um erro inesperado: {e}")