# app.py
import streamlit as st

# 🏛️ 1. CONFIGURAÇÃO OFICIAL UNIFICADA (OBRIGATORIAMENTE O PRIMEIRO COMANDO DO APP)
st.set_page_config(
    page_title="Portal Digital", 
    page_icon="🏛️", 
    layout="centered"
)

# 🎨 2. ESTILIZAÇÃO VISUAL (Cores do Templo + Ocultação Absoluta do Rodapé/GitHub/Menus)
st.html("""
    <style>
    /* Cores Originais do seu Projeto (Azul e Dourado) */
    .stApp { background-color: #0B1D3A; }
    h1, h2, h3, p, label, .stMarkdown { color: #FFFFFF !important; }
    div.stButton > button:first-child { background-color: #D4AF37 !important; color: #0B1D3A !important; font-weight: bold; width: 100%; border: none; }
    .card-frequencia { background-color: #12284C; padding: 15px; border-radius: 5px; border: 1px solid #D4AF37; margin-bottom: 10px; }
    .metrica-box { background-color: #12284C; padding: 20px; border-radius: 5px; border-left: 5px solid #D4AF37; text-align: center; }
    
    /* 🚫 REMOÇÃO TOTAL DA MARCA D'ÁGUA, GITHUB E COMPONENTES DO STREAMLIT CLOUD */
    footer { visibility: hidden !important; display: none !important; }
    [data-testid="stFooter"] { display: none !important; }
    header { visibility: hidden !important; display: none !important; }
    [data-testid="stHeader"] { display: none !important; }
    [data-testid="stToolbar"] { visibility: hidden !important; display: none !important; }
    .stAppDeployButton { display: none !important; }
    #MainMenu { visibility: hidden !important; display: none !important; }
    #GithubIcon { visibility: hidden !important; display: none !important; }
    
    /* Remove os links/badges flutuantes do painel de administração da hospedagem */
    .viewerBadge_link__1S137, .viewerBadge_text__1JaDK, [class^="viewerBadge"] {
        display: none !important;
    }
    </style>
""")

from supabase import create_client
from telas.aba_cadastro import renderizar_aba_cadastro
from telas.aba_frequencia import renderizar_aba_frequencia

# Link de Conexão com o seu Banco de Dados Supabase
SUPABASE_URL = "https://fklvpiltkvbmdturgdsa.supabase.co"
SUPABASE_KEY = "sb_publishable_LxS4fWewhz22TTy8wFDFEA_cVbfQ-eL"

# Conexão direta e estável
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Inicialização segura das variáveis de controle de acesso
if "logado" not in st.session_state: 
    st.session_state.logado = False
if "perfil_usuario" not in st.session_state: 
    st.session_state.perfil_usuario = "" # "admin" ou "irmao"
if "usuario_nome" not in st.session_state: 
    st.session_state.usuario_nome = ""
if "usuario_placet" not in st.session_state: 
    st.session_state.usuario_placet = None

# 🔒 3. TELA DE LOGIN: Exibida se o usuário não estiver logado
if not st.session_state.logado:
    st.markdown("<h1 style='text-align: center; letter-spacing: 4px;'>PORTAL DIGITAL</h1>", unsafe_allow_html=True)
    txt_placet = st.text_input("Número do Placet", placeholder="Digite seu registro ou 'admin'...", key="campo_login_placet")
    
    if st.button("ACESSAR ORIENTE", key="botao_login_oriente"):
        if txt_placet.lower() == "admin":
            st.session_state.logado = True
            st.session_state.perfil_usuario = "admin"
            st.session_state.usuario_nome = "Administrador"
            st.rerun()
        else:
            try:
                # Verifica se o Placet digitado existe na tabela quadro_irmaos
                resposta = supabase.table("quadro_irmaos").select("*").eq("placet", int(txt_placet)).execute()
                
                if resposta.data:
                    st.session_state.logado = True
                    st.session_state.perfil_usuario = "irmao"
                    st.session_state.usuario_nome = resposta.data[0].get("nome", "Irmão")
                    st.session_state.usuario_placet = int(txt_placet)
                    st.rerun()
                else:
                    st.error("Placet não encontrado no quadro da Loja.")
            except Exception as erro:
                st.error("Por favor, insira um número de Placet válido.")

# 🔓 4. ÁREA LOGADA
else:
    # Cria uma linha com colunas para alinhar o botão à direita no topo
    col_vazia, col_sair = st.columns([4, 1], vertical_alignment="center")
    
    # O botão de Sair fica na extrema direita, no topo absoluto da área logada
    if col_sair.button("Sair 🚪", key="botao_sair_sistema"):
        st.session_state.logado = False
        st.session_state.perfil_usuario = ""
        st.session_state.usuario_nome = ""
        st.session_state.usuario_placet = None
        st.rerun()
        
    # O nome do usuário (Administrador) aparece logo abaixo do botão
    st.markdown(f"### 🏛️ {st.session_state.usuario_nome}")
    st.divider() # Linha elegante separando o cabeçalho do conteúdo das abas

    # 🛠️ SEPARAÇÃO DE TELAS BASEADA DO PERFIL
    if st.session_state.perfil_usuario == "admin":
        # Administrador enxerga as duas abas normalmente
        aba_cadastro, aba_frequencia = st.tabs([
            "📝 Cadastrar Irmão / Reunião", 
            "📊 Livro de Frequência"
        ])
        with aba_cadastro: 
            renderizar_aba_cadastro(supabase)
        with aba_frequencia: 
            renderizar_aba_frequencia(supabase)
            
    elif st.session_state.perfil_usuario == "irmao":
        # Irmão comum entra em uma tela sem abas, direto para a função de frequência
        renderizar_aba_frequencia(supabase)
