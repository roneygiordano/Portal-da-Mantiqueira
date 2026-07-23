# frontend/main.py
import flet as ft
from telas.login import construir_tela_login

def main(page: ft.Page):
    layout_login = construir_tela_login(page)
    page.add(layout_login)

if __name__ == "__main__":
    # Atualizado de ft.app para ft.run conforme a nova versão
    ft.run(main, view=ft.AppView.WEB_BROWSER)
