import flet as ft
from components.signal_generator import SignalGenerator

class SensorsView:
    def __init__(self, page):
        self.page = page
        self.signal = SignalGenerator().generate()

    def go_back(self, e):
        self.page.go("/dashboard")

    def view(self):
        return ft.View(
            "/sensors",
            controls=[
                ft.AppBar(
                    title=ft.Text("Sensores"),
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
