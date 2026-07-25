# app.py
import streamlit as st

# 🏛️ 1. CONFIGURAÇÃO OFICIAL UNIFICADA
st.set_page_config(
    page_title="Portal Digital", 
    page_icon="🏛️", 
    layout="centered"
)

# 🎨 2. ESTILIZAÇÃO VISUAL + LIMPADOR AUTOMÁTICO VIA JAVASCRIPT
st.html("""
    <style>
    /* Cores Originais do seu Projeto (Azul e Dourado) */
    .stApp { background-color: #0B1D3A; }
    h1, h2, h3, p, label, .stMarkdown { color: #FFFFFF !important; }
    div.stButton > button:first-child { background-color: #D4AF37 !important; color: #0B1D3A !important; font-weight: bold; width: 100%; border: none; }
    .card-frequencia { background-color: #12284C; padding: 15px; border-radius: 5px; border: 1px solid #D4AF37; margin-bottom: 10px; }
    .metrica-box { background-color: #12284C; padding: 20px; border-radius: 5px; border-left: 5px solid #D4AF37; text-align: center; }
    
    /* Esconde cabeçalho e rodapé por padrão caso o CSS básico funcione */
    footer, header, [data-testid="stFooter"], [data-testid="stHeader"], [data-testid="stToolbar"] { 
        display: none !important; 
        visibility: hidden !important; 
    }
    </style>

    <script>
    // Função executada repetidamente para garantir que os elementos sejam apagados assim que surgirem
    const monitorarERemover = () => {
        // 1. Remove qualquer elemento HTML do tipo footer ou header
        document.querySelectorAll('footer, header, [data-testid="stFooter"], [data-testid="stHeader"]').forEach(el => {
            el.remove();
        });

        // 2. Procura por links que apontem para o Streamlit ou GitHub e remove o bloco inteiro deles
        document.querySelectorAll('a').forEach(link => {
            const href = link.href.toLowerCase();
            if (href.includes('streamlit.io') || href.includes('github.com')) {
                // Sobe até o container pai para apagar o botão ou badge por completo
                let container = link.closest('div') || link;
                if (container) container.remove();
            }
        });
        
        // 3. Remove especificamente o badge flutuante de visualização do Streamlit Cloud
        document.querySelectorAll('[class*="viewerBadge"]').forEach(badge => {
            badge.remove();
        });
    };

    # Executa a limpeza a cada 100 milissegundos para o usuário não ver nem o rastro das barras
    setInterval(monitorarERemover, 100);
    </script>
""")

from supabase import create_client
from telas.aba_cadastro import renderizar_aba_cadastro
from telas.aba_frequencia import renderizar_aba_frequencia
# ... O RESTANTE DO SEU CÓDIGO DO SUPABASE E LOGIN CONTINUA IGUAL ABAIXO ...
