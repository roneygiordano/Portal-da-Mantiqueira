# app.py
import streamlit as st

# 🏛️ CONFIGURAÇÃO OFICIAL: Define o nome do App e o ícone nativo
st.set_page_config(
    page_title="Portal Digital", 
    page_icon="https://icons8.com", # Link direto da imagem do templo
    layout="centered"
)

from supabase import create_client
from telas.aba_cadastro import renderizar_aba_cadastro
from telas.aba_frequencia import renderizar_aba_frequencia

# 1. Configuração Inicial da Página
st.set_page_config(page_title="Portal Digital", page_icon="🏛️", layout="centered")

# Estilização Visual Azul e Dourada original do seu projeto
st.markdown("""
    <style>
    .stApp { background-color: #0B1D3A; }
    h1, h2, h3, p, label, .stMarkdown { color: #FFFFFF !important; }
    div.stButton > button:first-child { background-color: #D4AF37 !important; color: #0B1D3A !important; font-weight: bold; width: 100%; border: none; }
    .card-frequencia { background-color: #12284C; padding: 15px; border-radius: 5px; border: 1px solid #D4AF37; margin-bottom: 10px; }
    .metrica-box { background-color: #12284C; padding: 20px; border-radius: 5px; border-left: 5px solid #D4AF37; text-align: center; }
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

# 🔒 3. TELA DE LOGIN: Exibida se o usuário não estiver logado
if not st.session_state.logado:
    
    # 📸 Adiciona a sua imagem centralizada acima do título
    # Ajuste o "logo.png" para o nome exato do seu arquivo
    st.image("maconaria.png", width=120, use_container_width=False)
    
    # Título centralizado com a fonte corrigida (sem quebras)
    st.markdown("<h2 style='text-align: center; font-size: 22px; font-weight: bold; letter-spacing: 2px; color: #FFFFFF; margin-bottom: 20px;'>PORTAL DIGITAL</h2>", unsafe_allow_html=True)
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

# 🔓 2. ÁREA LOGADA
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
        # Mas vamos passar o Placet dele para que a tela saiba que deve travar a visão
        renderizar_aba_frequencia(supabase)
