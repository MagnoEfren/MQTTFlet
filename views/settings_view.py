import flet as ft
from components.signal_generator import SignalGenerator

class SettingsView:
    def __init__(self, page):
        self.page = page
        self.signal = SignalGenerator().generate()

    def go_back(self, e):
        self.page.go("/dashboard")

    def view(self):
        return ft.View(
            "/settings",
            controls=[
                ft.AppBar(
                    title=ft.Text("Configuración"),
                    bgcolor=ft.colors.GREEN_700,
                    leading=ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=self.go_back),
                ),
                ft.Container(
                    #
                    padding=20,
                    expand=True
                )
            ]
        )
