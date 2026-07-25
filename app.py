# app.py
import streamlit as st

# 🏛️ 1. CONFIGURAÇÃO OFICIAL UNIFICADA (DEVE SER SEMPRE A PRIMEIRA INSTRUÇÃO DO SCRIPT)
st.set_page_config(
    page_title="Portal Digital", 
    page_icon="🏛️", 
    layout="centered"
)

from supabase import create_client
from telas.aba_cadastro import renderizar_aba_cadastro
from telas.aba_frequencia import renderizar_aba_frequencia

# 🎨 2. ESTILIZAÇÃO VISUAL (Cores do Templo + Ajuste de Layout + Ocultação do GitHub)
st.markdown("""
    <style>
    /* Força a centralização nativa do bloco de imagens do Streamlit */
    [data-testid="stImage"] {
        display: flex !important;
        justify-content: center !important;
        margin: 0 auto 15px auto !important;
    }
    
    /* Configurações visuais originais do seu projeto */
    .stApp { background-color: #0B1D3A; }
    h1, h2, h3, p, label, .stMarkdown { color: #FFFFFF !important; }
    div.stButton > button:first-child { background-color: #D4AF37 !important; color: #0B1D3A !important; font-weight: bold; width: 100%; border: none; }
    .card-frequencia { background-color: #12284C; padding: 15px; border-radius: 5px; border: 1px solid #D4AF37; margin-bottom: 10px; }
    .metrica-box { background-color: #12284C; padding: 20px; border-radius: 5px; border-left: 5px solid #D4AF37; text-align: center; }
    
    /* 🚫 NOVAS REGRAS: Remove o rodapé e o ícone do GitHub que leva ao repositório */
    footer, [data-testid="stFooter"], [data-testid="stConnectionStatus"] {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
    }
    
    /* Bloqueia especificamente os links e as classes do badge flutuante do GitHub */
    div[class*="viewerBadge"], 
    a[class*="viewerBadge"], 
    .viewerBadge_link__1S137, 
    a[href*="github.com"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }
    </style>
""", unsafe_allow_html=True)

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
import base64

# 🔒 3. TELA DE LOGIN: Exibida se o usuário não estiver logado
if not st.session_state.logado:
    
    # 🧠 Método seguro: Lê a imagem física do seu VS Code e converte em texto para o HTML
    try:
        with open("maconaria.png", "rb") as arquivo_imagem:
            imagem_bytes = arquivo_imagem.read()
            imagem_base64 = base64.b64encode(imagem_bytes).decode()
        
        # 📸 Renderiza a imagem e o título 100% centralizados no computador e no celular
        st.html(f"""
            <div style="text-align: center; margin-bottom: 15px;">
                <img src="data:image/png;base64,{imagem_base64}" style="width: 70px; height: auto;">
                <h2 style='font-size: 30px; font-weight: bold; letter-spacing: 2px; color: #FFFFFF; margin: 15px 0 20px 0;'>PORTAL 219 DIGITAL</h2>
            </div>
        """)
    except FileNotFoundError:
        # Caso o arquivo não seja encontrado no GitHub, exibe apenas o título para não travar o app
        st.markdown("<h2 style='text-align: center; font-size: 22px; font-weight: bold; letter-spacing: 2px; color: #FFFFFF; margin-bottom: 20px;'>PORTAL DIGITAL</h2>", unsafe_allow_html=True)
        st.warning("Aviso: O arquivo 'maconaria.png' não foi encontrado na raiz do projeto.")
    
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
    # Cabeçalho com o nome de quem entrou e o botão de Sair
    col_t, col_s = st.columns([4, 1])
    col_t.markdown(f"### 🏛️ {st.session_state.usuario_nome}")
    
    if col_s.button("Sair 🚪", key="botao_sair_sistema"):
        st.session_state.logado = False
        st.session_state.perfil_usuario = ""
        st.session_state.usuario_nome = ""
        st.session_state.usuario_placet = None
        st.rerun()

    # 🛠️ SEPARAÇÃO DE TELAS BASEADA NO PERFIL
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
