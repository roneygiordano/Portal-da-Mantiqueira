import flet as ft
from telas.login import construir_tela_login

def main(page: ft.Page):
    layout_login = construir_tela_login(page)
    page.add(layout_login)

if __name__ == "__main__":
    ft.app(target=main)
