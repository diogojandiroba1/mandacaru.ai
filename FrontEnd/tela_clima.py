import streamlit as st
import plotly.graph_objects as go
import numpy as np

def show_page():
    st.title("Status Geral e Condições Atuais")
    
    # Cards de Status
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("""
        <div style="background-color:#FFF3E0; padding:15px; border-left:5px solid #FF9800; border-radius:5px;">
            <h3 style="color:#F57C00; margin:0;">⚠️ ATENÇÃO</h3>
            <p><b>Estresse Hídrico Moderado em Milho</b></p>
            <small>Atualizado: Hoje, 13:00h</small>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown("""
        <div style="background-color:#E8F5E9; padding:15px; border-left:5px solid #4CAF50; border-radius:5px;">
            <h3 style="color:#388E3C; margin:0;">🌤️ Clima: 28°C</h3>
            <p style="margin:0;">📍 Fazenda Canudos, BA</p>
            <ul style="font-size:0.8em; padding-left:15px; margin:5px 0;">
                <li>Umidade Ar: 65%</li>
                <li>Vento: 15 km/h N</li>
                <li>Chuva (48h): 0 mm</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with c3:
        st.info("📅 **PRÓXIMOS EVENTOS**")
        st.markdown("""
        - 27/11: Aplicação de Ureia
        - 29/11: Colheita Sorgo
        - **⚠️ 02/12: Alerta Geada (Prev)**
        """)
        
    st.markdown("---")
    st.subheader("Análise Detalhada")
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("**Umidade do Solo (%)**")
        # Gráfico Simulado
        fig1 = go.Figure(go.Scatter(y=np.random.randint(40, 60, 7), x=['Seg','Ter','Qua','Qui','Sex','Sab','Dom'], 
                                    mode='lines+markers', line=dict(color='#8BC34A')))
        fig1.update_layout(height=300, margin=dict(l=20,r=20,t=20,b=20))
        st.plotly_chart(fig1, use_container_width=True)
        
    with col_chart2:
        st.markdown("**Temp vs Evapotranspiração**")
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(y=[28,29,30,27,26], x=['Seg','Ter','Qua','Qui','Sex'], name='Temp', marker_color='#FFCC80'))
        fig2.add_trace(go.Scatter(y=[4,5,5,4,3], x=['Seg','Ter','Qua','Qui','Sex'], name='ETC', yaxis='y2', line=dict(color='blue')))
        fig2.update_layout(yaxis2=dict(overlaying='y', side='right'), height=300, margin=dict(l=20,r=20,t=20,b=20), showlegend=True)
        st.plotly_chart(fig2, use_container_width=True)