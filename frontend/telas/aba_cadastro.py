# frontend/telas/aba_cadastro.py
import streamlit as st
from datetime import date

def renderizar_aba_cadastro(supabase):
    st.subheader("👥 Cadastrar Novo Irmão no Quadro")
    
    with st.form("form_cadastro_irmao", clear_on_submit=True):
        novo_nome = st.text_input("Nome Completo do Irmão")
        novo_placet = st.number_input("Número do Placet", min_value=1, step=1, value=219001)
        btn_salvar_irmao = st.form_submit_button("Salvar Irmão na Base")
        
        if btn_salvar_irmao:
            if not novo_nome:
                st.warning("Por favor, preencha o nome.")
            else:
                try:
                    dados = {"nome": novo_nome, "lugar": novo_placet, "situação": "Presença"}
                    supabase.table("PortalDigital").insert(dados).execute()
                    st.success(f"Ir.'. {novo_nome} cadastrado com sucesso!")
                except Exception as erro:
                    st.error(f"Erro ao salvar no banco: {erro}")

    st.write("---")
    st.subheader("📅 Lançar Nova Reunião para Todos os Irmãos")
    st.write("Selecione a data abaixo para criar a folha de presença automática.")
    
    data_selecionada = st.date_input("Data da Reunião", value=date.today())
    
    if st.button("🚀 Gerar Chamada Geral para esta Data"):
        try:
            todos_irmaos = supabase.table("PortalDigital").select("nome", "lugar").execute()
            if not todos_irmaos.data:
                st.warning("Não há irmãos cadastrados no banco.")
            else:
                lista_limpa = {v['lugar']: v['nome'] for v in todos_irmaos.data}
                contador = 0
                for placet_id, nome_id in lista_limpa.items():
                    nova_linha = {
                        "nome": nome_id,
                        "lugar": placet_id,
                        "dados_reuniao": str(data_selecionada),
                        "situação": "Presença"
                    }
                    supabase.table("PortalDigital").insert(nova_linha).execute()
                    contador += 1
                st.success(f"Sucesso! Gerada folha de presença para {contador} irmãos!")
        except Exception as erro:
            st.error(f"Erro ao gerar reunião: {erro}")
