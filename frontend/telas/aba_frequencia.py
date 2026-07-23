# frontend/telas/aba_frequencia.py
import streamlit as st
from datetime import datetime

def renderizar_aba_frequencia(supabase):
    st.subheader("Controle de Presença Real")
    st.write("Abaixo estão os registros puxados diretamente do Supabase:")
    
    try:
        dados_reais = supabase.table("PortalDigital").select("*").order("dados_reuniao", desc=True).execute()
        if not dados_reais.data:
            st.info("Nenhum registro de reunião foi encontrado.")
        else:
            for reg in dados_reais.data:
                nome = reg.get("nome", "Desconhecido")
                placet = reg.get("lugar", "N/A")
                data_banco = reg.get("dados_reuniao", "Sem Data")
                sit = reg.get("situação", "Presença")
                
                data_formatada = "Sem Data"
                if data_banco and data_banco != "Sem Data":
                    try:
                        data_formatada = datetime.strptime(data_banco, "%Y-%m-%d").strftime("%d/%m/%Y")
                    except:
                        data_formatada = data_banco
                
                cor = "#2ECC71" if sit == "Presença" else ("#E74C3C" if sit == "Falta" else "#F1C40F")
                
                st.markdown(f"""
                <div class='card-frequencia'>
                    <p><strong>Nome:</strong> {nome} | <strong>Placet:</strong> {placet}</p>
                    <p><strong>Data da Reunião:</strong> {data_formatada}</p>
                    <p><strong>Situação:</strong> <span style='color: {cor};'>● {sit}</span></p>
                </div>
                """, unsafe_allow_html=True)
    except Exception as erro:
        st.error(f"Erro ao carregar frequências: {erro}")
