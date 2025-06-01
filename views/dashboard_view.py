import flet as ft

class DashboardView:
    def __init__(self, page):
        self.page = page
        self.green = "#06f998"

    def go_to_graph(self, e):
        self.page.go("/graph")

    def go_to_sensors(self, e):
        self.page.go("/sensors")

    def go_to_motor(self, e):
        self.page.go("/motor")

    def go_to_settings(self, e):
        self.page.go("/settings")

    def logout(self, e):
        self.page.go("/")  # Regresar a login

    def view(self):
        return ft.View(
            "/dashboard",
            controls=[
                ft.AppBar(
                    title=ft.Text("Control y Monitoreo", color="black", weight="bold"),
                    bgcolor=self.green,
                    actions=[
                        ft.IconButton(
                            icon=ft.icons.LOGOUT,
                            icon_color="black",
                            tooltip="Salir",
                            on_click=self.logout
                        )
                    ]
                ),
                 ft.Column(
                     controls=[
                         ft.TextButton("sensores",  on_click=self.go_to_sensors),
                         ft.TextButton("grafica",  on_click=self.go_to_graph),
                         ft.TextButton("motor",  on_click=self.go_to_motor),
                         ft.TextButton("setings",  on_click=self.go_to_settings),
                     ]
                 )
            ]
        )
