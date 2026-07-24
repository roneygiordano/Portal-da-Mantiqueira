# telas/aba_cadastro.py
import streamlit as st
from datetime import date

def renderizar_aba_cadastro(supabase):
    st.subheader("👥 Cadastrar Irmão")
    
    with st.form("form_cadastro_irmao", clear_on_submit=True):
        novo_nome = st.text_input("Nome Completo do Irmão")
        novo_placet = st.number_input("Número do Placet", min_value=1, step=1, value=219001)
        btn_salvar_irmao = st.form_submit_button("Salvar Irmão no Quadro")
        
        if btn_salvar_irmao:
            if not novo_nome:
                st.warning("Por favor, preencha o nome.")
            else:
                try:
                    # 🔍 TRAVA 1: Verifica se já existe um irmão com o mesmo Nome
                    busca_nome = supabase.table("quadro_irmaos").select("nome").eq("nome", novo_nome.strip()).execute()
                    
                    # 🔍 TRAVA 2: Verifica se já existe um irmão com o mesmo Placet
                    busca_placet = supabase.table("quadro_irmaos").select("placet").eq("placet", int(novo_placet)).execute()
                    
                    if busca_nome.data:
                        st.error(f"⚠️ Atenção: Já existe um irmão cadastrado com o nome '{novo_nome}'!")
                    elif busca_placet.data:
                        st.error(f"⚠️ Atenção: O número de Placet '{novo_placet}' já está sendo usado por outro irmão!")
                    else:
                        # Se passou pelas duas travas, salva com segurança
                        dados = {"nome": novo_nome.strip(), "placet": int(novo_placet)}
                        supabase.table("quadro_irmaos").insert(dados).execute()
                        st.success(f"Ir.'. {novo_nome} adicionado ao Quadro da Loja!")
                        
                except Exception as erro:
                    st.error(f"Erro ao acessar o banco de dados: {erro}")

    st.write("---")
    st.subheader("📅 Lançar Nova Reunião")
    st.write("Cria uma pauta de chamada única para a data selecionada.")
    
    data_selecionada = st.date_input("Data da Reunião", value=date.today(), format="DD/MM/YYYY")
    
    if st.button("🚀 Gerar Chamada para esta Data"):
        try:
            # 🔍 TRAVA 3: Verifica se já existe QUALQUER registro de chamada lançado para esta data
            busca_reuniao = supabase.table("livro_presencas").select("id").eq("data_reuniao", str(data_selecionada)).execute()
            
            if busca_reuniao.data:
                data_br = data_selecionada.strftime('%d/%m/%Y')
                st.error(f"⚠️ A reunião da data {data_br} já foi lançada anteriormente! Você pode editá-la diretamente na aba 'Livro de Frequência'.")
            else:
                # Puxa o quadro atual de irmãos para gerar a chamada
                quadro = supabase.table("quadro_irmaos").select("placet").execute()
                
                if not quadro.data:
                    st.warning("Não há irmãos cadastrados no Quadro para gerar a chamada.")
                else:
                    contador = 0
                    for irmao in quadro.data:
                        placet_id = irmao.get("placet")
                        
                        nova_presenca = {
                            "placet_irmao": int(placet_id),
                            "data_reuniao": str(data_selecionada),
                            "situacao": "Presença"
                        }
                        supabase.table("livro_presencas").insert(nova_presenca).execute()
                        contador += 1
                        
                    data_br = data_selecionada.strftime('%d/%m/%Y')
                    st.success(f"Sucesso! Reunião de {data_br} lançada para {contador} obreiros!")
                    
        except Exception as erro:
            st.error(f"Erro ao gerar reunião: {erro}")
