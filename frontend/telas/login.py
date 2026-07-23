import flet as ft
from core.cores import FUNDO_ESCURO, DOURADO_MACONICO, TEXTO_BRANCO, TEXTO_CINZA

def construir_tela_login(page: ft.Page):
    page.title = "Portal Digital - Login"
    page.background_color = FUNDO_ESCURO
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.update()

    # Inputs de texto
    txt_cim = ft.TextField(
        label="CIM / Registro",
        label_style=ft.TextStyle(color=DOURADO_MACONICO),
        border_color=TEXTO_CINZA,
        focused_border_color=DOURADO_MACONICO,
        color=TEXTO_BRANCO,
        width=300
    )

    txt_senha = ft.TextField(
        label="Palavra de Passe",
        label_style=ft.TextStyle(color=DOURADO_MACONICO),
        border_color=TEXTO_CINZA,
        focused_border_color=DOURADO_MACONICO,
        color=TEXTO_BRANCO,
        password=True,
        can_reveal_password=True,
        width=300
    )

    def efetuar_login(e):
        if not txt_cim.value or not txt_senha.value:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor, preencha todos os campos."))
            page.snack_bar.open = True
        else:
            # Mensagem provisória enquanto o backend não está pronto
            page.snack_bar = ft.SnackBar(ft.Text(f"Conectando ao backend para validar o Ir.'. {txt_cim.value}..."))
            page.snack_bar.open = True
        page.update()

    btn_acessar = ft.ElevatedButton(
        text="ACESSAR ORIENTE",
        color=FUNDO_ESCURO,
        bgcolor=DOURADO_MACONICO,
        width=300,
        height=45,
        on_click=efetuar_login,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=5),
        )
    )

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("PORTAL DIGITAL", size=28, weight=ft.FontWeight.W_300, color=TEXTO_BRANCO, letter_spacing=4),
                ft.Text("Oficina 219", size=14, color=TEXTO_CINZA, letter_spacing=2),
                ft.Container(height=20),
                txt_cim,
                ft.Container(height=10),
                txt_senha,
                ft.Container(height=20),
                btn_acessar
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        alignment=ft.alignment.center
    )
