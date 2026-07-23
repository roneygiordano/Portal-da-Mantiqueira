# notificacoes.py
import requests

# 🔐 Quando você contratar o seu provedor de WhatsApp, você preenche aqui uma única vez
API_URL = "https://seuprovedor.com" 
TOKEN = "SEU_TOKEN_AQUI"

def enviar_mensagem_whatsapp(numero, texto):
    """
    Função centralizada para enviar mensagens de WhatsApp em segundo plano.
    """
    # Se ainda não configurou o TOKEN, a função apenas avisa o console e não trava o app
    if TOKEN == "SEU_TOKEN_AQUI":
        print(f"[Simulação SMS/Whats] Para o número {numero}: {texto}")
        return

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TOKEN}"
    }
    
    # Limpa o número deixando apenas dígitos (remove parênteses, traços e espaços)
    numero_limpo = "".join(filter(str.isdigit, str(numero)))
    
    # Garante o código do Brasil (55) na frente do número
    if not numero_limpo.startswith("55"):
        numero_limpo = f"55{numero_limpo}"
        
    payload = {
        "number": numero_limpo,
        "message": texto
    }
    
    try:
        # Timeout de 5 segundos para garantir que a tela do Streamlit nunca trave se a API oscilar
        requests.post(API_URL, json=payload, headers=headers, timeout=5)
    except Exception as e:
        print(f"Erro ao enviar mensagem para {numero_limpo}: {e}")
