# frontend/telas/login.py
import flet as ft
from core.cores import FUNDO_ESCURO, DOURADO_MACONICO, TEXTO_BRANCO, TEXTO_CINZA
from core.config import supabase

def construir_tela_login(page: ft.Page):
    page.title = "Portal Digital - Login"
    page.background_color = FUNDO_ESCURO
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.update()

    # Campo para o Placet
    txt_placet = ft.TextField(
        label="Número do Placet",
        label_style=ft.TextStyle(color=DOURADO_MACONICO),
        border_color=TEXTO_CINZA,
        focused_border_color=DOURADO_MACONICO,
        color=TEXTO_BRANCO,
        width=300
    )

    def efetuar_login(e):
        if not txt_placet.value:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor, digite o número do seu Placet."))
            page.snack_bar.open = True
            page.update()
            return

        try:
            # Busca na sua tabela do Supabase buscando pelo número do placet
            resposta = supabase.table("PortalDigital").select("*").eq("lugar", txt_placet.value).execute()
            
            if resposta.data:
                irmao = resposta.data[0] # Pega o primeiro irmão encontrado na lista
                nome_irmao = irmao.get("nome", "Irmão")
                situacao_irmao = irmao.get("situação", "Não informada")
                
                page.snack_bar = ft.SnackBar(
                    ft.Text(f"Bem-vindo, Ir.'. {nome_irmao}! Situação: {situacao_irmao}")
                )
                page.snack_bar.open = True
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Placet não encontrado no quadro da Loja."))
                page.snack_bar.open = True
                
        except Exception as erro:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao conectar ao banco: {erro}"))
            page.snack_bar.open = True
            
        page.update()

    # Botão com a sintaxe correta e limpa para evitar conflitos de versão
    btn_acessar = ft.ElevatedButton(
        content=ft.Text("ACESSAR ORIENTE", color=FUNDO_ESCURO, weight=ft.FontWeight.BOLD),
        bgcolor=DOURADO_MACONICO,
        width=300,
        height=45,
        on_click=efetuar_login,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=5)
        )
    )

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("PORTAL DIGITAL", size=28, weight=ft.FontWeight.W_300, color=TEXTO_BRANCO, letter_spacing=4),
                ft.Text("Oficina 219", size=14, color=TEXTO_CINZA, letter_spacing=2),
                ft.Container(height=20),
                txt_placet,
                ft.Container(height=20),
                btn_acessar
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        alignment=ft.alignment.center
    )
