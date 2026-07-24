# telas/aba_frequencia.py
import streamlit as st
import pandas as pd
from datetime import datetime

def renderizar_aba_frequencia(supabase):
        # Injeta o CSS customizado logo no início da aba para travar o layout do celular
    st.markdown(
        """
        <style>
        /* Remove o espaçamento exagerado padrão do Streamlit entre colunas */
        [data-testid="stHorizontalBlock"] {
            gap: 8px !important;
        }
        
        /* Força as colunas a ficarem lado a lado (50% de largura cada) */
        [data-testid="column"] {
            flex: 1 1 calc(50% - 4px) !important;
            min-width: 45% !important;
        }

        /* Reduz o tamanho da fonte das métricas apenas em telas pequenas para não quebrar linha */
        @media (max-width: 640px) {
            [data-testid="stMetricLabel"] {
                font-size: 0.85rem !important;
            }
            [data-testid="stMetricValue"] {
                font-size: 1.4rem !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )


    st.subheader("📊 Livro de Frequência")
    
    # Captura os dados de sessão definidos no login (app.py)
    perfil_atual = st.session_state.get("perfil_usuario", "irmao")
    placet_logado = st.session_state.get("usuario_placet")
    nome_logado = st.session_state.get("usuario_nome")
    
    # Tradução dos meses para o português
    MESES_NOME = {
        "01": "Janeiro", "02": "Fevereiro", "03": "Março", "04": "Abril",
        "05": "Maio", "06": "Junho", "07": "Julho", "08": "Agosto",
        "09": "Setembro", "10": "Outubro", "11": "Novembro", "12": "Dezembro"
    }
    
    try:
        # Busca inicial nas tabelas do Supabase
        irmaos = supabase.table("quadro_irmaos").select("*").execute()
        chamadas = supabase.table("livro_presencas").select("*").execute()
        
        if not irmaos.data:
            st.info("Nenhum irmão cadastrado no quadro.")
            return
            
        # =======================================================
        # 🎯 PARTE 1: MÉTRICAS DO TOPO (MÉTRICAS DO ANO ATUAL)
        # =======================================================
        st.write("### 🔍 Resumo")
        
        if perfil_atual == "admin":
            # Administrador escolhe qual irmão quer analisar
            nomes_lista = sorted([str(i["nome"]).strip() for i in irmaos.data if i.get("nome")])
            nome_selecionado = st.selectbox(
                "Selecione o Irmão para analisar:", 
                options=nomes_lista, 
                key="sb_assiduidade_frequencia"
            )
            irmao_atual = next((i for i in irmaos.data if str(i.get("nome", "")).strip() == nome_selecionado), None)
            placet_atual = irmao_atual.get("placet") if irmao_atual else ""
        else:
            # Irmão comum fica travado no próprio perfil
            nome_selecionado = nome_logado
            placet_atual = placet_logado
            st.info(f"Exibindo métricas pessoais do Ir.'. **{nome_selecionado}** (Placet: `{placet_atual}`)")
        
        # Processamento de contagem das presenças
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
                
                if placet_reuniao is not None and str(placet_reuniao).strip() == str(placet_atual).strip():
                    if data_b and str(data_b).startswith(ano_atual):
                        total_reunioes += 1
                        if sit == "Presença": total_presencas += 1
                        elif sit == "Falta": total_faltas += 1
                        elif sit == "Justificada": total_justificadas += 1
                        
        porcentagem = (total_presencas / total_reunioes) * 100 if total_reunioes > 0 else 0.0
        
        # --- LINHA 1 DO DASHBOARD (2 Colunas) ---
        l1_c1, l1_c2 = st.columns(2)
        l1_c1.metric(label="📅 Reuniões", value=f"{total_reunioes}")
        l1_c2.metric(label="🟢 Presenças", value=f"{total_presencas}")

        # --- LINHA 2 DO DASHBOARD (2 Colunas) ---
        l2_c1, l2_c2 = st.columns(2)
        l2_c1.metric(label="🔴 Faltas", value=f"{total_faltas}")
        l2_c2.metric(label="🟡 Justificadas", value=f"{total_justificadas}")

        # --- LINHA 3 DO DASHBOARD (Porcentagem Centralizada) ---
        # Criamos uma coluna central para destacar a métrica principal
        _, col_centro, _ = st.columns([1, 2, 1])
        col_centro.metric(label="📈 Porcentagem de Assiduidade", value=f"{porcentagem:.1f}%")
        
        st.write("---") 
        
        # =======================================================
        # 📊 PARTE 2: HISTÓRICO DE REUNIÕES E FILTRO DE MÊS
        # =======================================================
        st.write("### 📅 Histórico por Mês")
        
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
                    "Placet_Irmao": placet,
                    "Data": data_coluna,
                    "Mes_Filtro": data_b[5:7] if data_b else "", 
                    "Ano_Filtro": data_b[0:4] if data_b else "", 
                    "Situacao": sinal
                })
                
                mapa_ids_banco[(nome_irmao, data_coluna)] = id_banco

        # Renderização do seletor de mês na tela
        lista_meses_ordenada = sorted(list(meses_disponiveis_no_banco), key=lambda x: (x[1], x[0]), reverse=True)
        opcoes_filtro = ["Exibir Todas as Reuniões"] + [item[2] for item in lista_meses_ordenada]
        mes_selecionado = st.selectbox("Selecione o mês que deseja visualizar:", opcoes_filtro, key="filtro_mes_geral")

        # Filtra os registros baseados no mês escolhido
        dados_filtrados = dados_brutos
        if mes_selecionado != "Exibir Todas as Reuniões":
            for mm, yyyy, nome_ma in lista_meses_ordenada:
                if nome_ma == mes_selecionado:
                    dados_filtrados = [d for d in dados_brutos if d["Mes_Filtro"] == mm and d["Ano_Filtro"] == yyyy]
                    break

        # 🛠========= EXIBIÇÃO DIFERENCIADA POR PERFIL =========
        if perfil_atual == "admin":
            st.write("📝 *Modo Editor: Altere as presenças diretamente na planilha abaixo.*")
            df_final = pd.DataFrame([{"Nome do Irmão": nome} for nome in mapa_placet_nome.values()])
            
            if dados_filtrados:
                df_bruto = pd.DataFrame(dados_filtrados).drop_duplicates(subset=["Nome do Irmão", "Data"])
                df_pauta = df_bruto.pivot(index="Nome do Irmão", columns="Data", values="Situacao").reset_index()
                
                colunas_datas = [c for c in df_pauta.columns if c != "Nome do Irmão"]
                colunas_datas.sort(key=lambda date: datetime.strptime(date, "%d/%m/%Y"))
                df_pauta = df_pauta[["Nome do Irmão"] + colunas_datas]
                
                df_final = pd.merge(df_final, df_pauta, on="Nome do Irmão", how="left")
                
            df_final = df_final.fillna("⚪ Sem Registro")
            
            config_col = {"Nome do Irmão": st.column_config.TextColumn("Nome do Irmão", disabled=True)}
            for col in [c for c in df_final.columns if c != "Nome do Irmão"]:
                config_col[col] = st.column_config.SelectboxColumn(col, options=["🟢 Presença", "🔴 Falta", "🟡 Justificada", "⚪ Sem Registro"], required=True)
                
            df_editado = st.data_editor(df_final, column_config=config_col, use_container_width=True, hide_index=True, key="editor_frequencia")
            
    except Exception as e:
        st.error(f"Erro ao carregar o livro de frequência: {e}")
