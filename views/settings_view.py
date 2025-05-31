import flet as ft
 
class SettingsView:
    def __init__(self, page):
        self.page = page
   
    def go_back(self, e):
        self.page.go("/dashboard")

    def view(self):
        return ft.View(
            "/settings",
            controls=[
                ft.AppBar(
                    title=ft.Text("Configuración"),
                    bgcolor="green",
                    leading=ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=self.go_back),
                ),
                ft.Container(
                    content=ft.Text("Vista de prueba funcionando."),
                    padding=20,
                    expand=True
                )
            ]
        )
