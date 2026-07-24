# telas/aba_frequencia.py
import streamlit as st
import pandas as pd
from datetime import datetime

def renderizar_aba_frequencia(supabase):
    st.subheader("📊 Livro de Frequência Interativo")
    
    # Dicionário para traduzir o número do mês para o nome em português
    MESES_NOME = {
        "01": "Janeiro", "02": "Fevereiro", "03": "Março", "04": "Abril",
        "05": "Maio", "06": "Junho", "07": "Julho", "08": "Agosto",
        "09": "Setembro", "10": "Outubro", "11": "Novembro", "12": "Dezembro"
    }
    
    try:
        # Puxa as tabelas fazendo o cruzamento correto dos dados
        irmaos = supabase.table("quadro_irmaos").select("*").execute()
        chamadas = supabase.table("livro_presencas").select("*").execute()
        
        if not irmaos.data:
            st.info("Nenhum irmão cadastrado no quadro.")
            return
            
        # =======================================================
        # 🎯 NOVO PAINEL DE ASSIDUIDADE (INTEGRADO NA FREQUÊNCIA)
        # =======================================================
        st.write("### 🔍 Consulta Rápida de Assiduidade")
        
        # Extrai e ordena os nomes do cadastro para a guia suspensa
        nomes_lista = sorted([str(i["nome"]).strip() for i in irmaos.data if i.get("nome")])
        
        nome_selecionado = st.selectbox(
            "Selecione o Irmão para ver o resumo de faltas e presenças:", 
            options=nomes_lista, 
            key="sb_assiduidade_frequencia"
        )
        
        # Descobre o Placet do irmão selecionado
        irmao_atual = next((i for i in irmaos.data if str(i.get("nome", "")).strip() == nome_selecionado), None)
        placet_atual = irmao_atual.get("placet") if irmao_atual else ""
        
        # Contadores das métricas do Ano Corrente
        ano_atual = str(datetime.now().year)
        total_reunioes = 0
        total_presencas = 0
        total_faltas = 0
        total_justificadas = 0
        
        if chamadas.data:
            for ch in chamadas.data:
                placet_reuniao = ch.get("placet_irmao")
                data_b = ch.get("data_reuniao")
                sit = ch.get("situacao", "Presença")
                
                # Se o placet bater com o irmão selecionado e for deste ano, soma na estatística
                if placet_reuniao is not None and str(placet_reuniao).strip() == str(placet_atual).strip():
                    if data_b and str(data_b).startswith(ano_atual):
                        total_reunioes += 1
                        if sit == "Presença": total_presencas += 1
                        elif sit == "Falta": total_faltas += 1
                        elif sit == "Justificada": total_justificadas += 1
                        
        # Cálculo seguro da porcentagem (%) para evitar divisão por zero
        porcentagem = (total_presencas / total_reunioes) * 100 if total_reunioes > 0 else 0.0
        
        # Exibe os 5 blocos de resultados lado a lado na tela
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1: st.metric(label="📅 Reuniões", value=f"{total_reunioes}")
        with col2: st.metric(label="🟢 Presenças", value=f"{total_presencas}")
        with col3: st.metric(label="🔴 Faltas", value=f"{total_faltas}")
        with col4: st.metric(label="🟡 Justificadas", value=f"{total_justificadas}")
        with col5: st.metric(label="📈 Porcentagem", value=f"{porcentagem:.1f}%")
        
        st.write("---") # Linha divisória para separar o painel da planilha abaixo
        
        # =======================================================
        # SEU CÓDIGO ORIGINAL DA PLANILHA DINÂMICA DAQUI PARA BAIXO
        # =======================================================
        st.write("### 📝 Livro de Presenças Geral")
        
        # Cria dicionários de apoio para o Python linkar Placet -> Nome
        mapa_placet_nome = {i['placet']: i['nome'] for i in irmaos.data}
        mapa_ids_banco = {}
        
        dados_brutos = []
        meses_disponiveis_no_banco = set() 
        
        if chamadas.data:
            for ch in chamadas.data:
                id_banco = ch.get("id")
                placet = ch.get("placet_irmao")
                data_b = ch.get("data_reuniao") 
                sit = ch.get("situacao", "Presença")
                
                nome_irmao = mapa_placet_nome.get(placet, f"Placet {placet}")
                
                if data_b and data_b != "None":
                    try:
                        objeto_data = datetime.strptime(data_b, "%Y-%m-%d")
                        num_mes = objeto_data.strftime("%m")
                        ano = objeto_data.strftime("%Y")
                        nome_mes_ano = f"{MESES_NOME[num_mes]} / {ano}"
                        meses_disponiveis_no_banco.add((data_b[5:7], ano, nome_mes_ano)) 
                    except:
                        pass
                
                try:
                    data_coluna = datetime.strptime(data_b, "%Y-%m-%d").strftime("%d/%m/%Y")
                except:
                    data_coluna = data_b
                
                sinal = "🟢 Presença"
                if sit == "Falta": sinal = "🔴 Falta"
                elif sit == "Justificada": sinal = "🟡 Justificada"
                
                dados_brutos.append({
                    "Nome do Irmão": nome_irmao,
                    "Data": data_coluna,
                    "Mes_Filtro": data_b[5:7] if data_b else "", 
                    "Ano_Filtro": data_b[0:4] if data_b else "", 
                    "Situacao": sinal
                })
                
                mapa_ids_banco[(nome_irmao, data_coluna)] = id_banco

        st.write("#### 🔍 Filtrar Pauta")
        
        # Correção inteligente para evitar falhas ao ordenar a lista de meses
        lista_meses_ordenada = sorted(list(meses_disponiveis_no_banco), key=lambda x: (x[1], x[0]), reverse=True)
        opcoes_filtro = ["Exibir Todas as Reuniões"] + [item[2] for item in lista_meses_ordenada]
        
        mes_selecionado = st.selectbox("Selecione o mês das sessões que deseja visualizar:", opcoes_filtro)

        dados_filtrados = dados_brutos
        
        if mes_selecionado != "Exibir Todas as Reuniões":
            for mm, yyyy, nome_ma in lista_meses_ordenada:
                if nome_ma == mes_selecionado:
                    dados_filtrados = [d for d in dados_brutos if d["Mes_Filtro"] == mm and d["Ano_Filtro"] == yyyy]
                    break

        df_final = pd.DataFrame([{"Nome do Irmão": nome} for nome in mapa_placet_nome.values()])
        
        if dados_filtrados:
            df_bruto = pd.DataFrame(dados_filtrados).drop_duplicates(subset=["Nome do Irmão", "Data"])
            df_pauta = df_bruto.pivot(index="Nome do Irmão", columns="Data", values="Situacao").reset_index()
            
            colunas_datas = [c for c in df_pauta.columns if c != "Nome do Irmão"]
            colunas_datas.sort(key=lambda date: datetime.strptime(date, "%d/%m/%Y"))
            df_pauta = df_pauta[["Nome do Irmão"] + colunas_datas]
            
            df_final = pd.merge(df_final, df_pauta, on="Nome do Irmão", how="left")
            
        df_final = df_final.fillna("⚪ Sem Registro")
        
        colunas_finais_datas = [col for col in df_final.columns if col != "Nome do Irmão"]
        config_col = {"Nome do Irmão": st.column_config.TextColumn("Nome do Irmão", disabled=True)}
        
        for col in colunas_finais_datas:
            config_col[col] = st.column_config.SelectboxColumn(col, options=["🟢 Presença", "🔴 Falta", "🟡 Justificada", "⚪ Sem Registro"], required=True)
            
        df_editado = st.data_editor(df_final, column_config=config_col, use_container_width=True, hide_index=True, key="editor_frequencia")
        
        if st.session_state.editor_frequencia and "edited_rows" in st.session_state.editor_frequencia:
            alteracoes = st.session_state.editor_frequencia["edited_rows"]
            for idx, col_alteradas in alteracoes.items():
                nome_alt = df_final.iloc[idx]["Nome do Irmão"]
                for dt_alt, val_sinal in col_alteradas.items():
                    id_banco = mapa_ids_banco.get((nome_alt, dt_alt))
                    
                    status_puro = "Presença"
                    if "Falta" in val_sinal: status_puro = "Falta"
                    elif "Justificada" in val_sinal: status_puro = "Justificada"
                    
                    if id_banco:
                        supabase.table("livro_presencas").update({"situacao": status_puro}).eq("id", id_banco).execute()
                        st.toast(f"Frequência de {nome_alt} updated!", icon="💾")
            st.rerun()
            
    except Exception as e:
        st.error("Erro ao processar pauta.")
        st.code(e)
