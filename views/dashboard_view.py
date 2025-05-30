import flet as ft

class DashboardView:
    def __init__(self, page):
        self.page = page

    def go_to_graph(self, e):
        self.page.go("/graph")

    def logout(self, e):
        self.page.go("/")  # Regresar a login

    def view(self):
        return ft.View(
            "/dashboard",
            controls=[
                ft.AppBar(
                    title=ft.Text("Dashboard IoT"),
                    bgcolor=ft.colors.GREEN_700,
                    actions=[
                        ft.IconButton(icon=ft.icons.LOGOUT, tooltip="Salir", on_click=self.logout)
                    ]
                ),
                ft.Column(
                    [
                        ft.Text("Selecciona una opción:", size=20, weight=ft.FontWeight.W_600),
                        ft.ElevatedButton("Dispositivos", icon=ft.icons.DEVICES),
                        ft.ElevatedButton("Sensores", icon=ft.icons.SENSOR_DOOR),
                        ft.ElevatedButton("Automatización", icon=ft.icons.AUTO_MODE),
                        ft.ElevatedButton("Actividad", icon=ft.icons.HISTORY),
                        ft.ElevatedButton("Ver Gráfica Analógica", icon=ft.icons.SHOW_CHART, on_click=self.go_to_graph)
                    ],
                    spacing=15,
                    expand=True
                )
            ]
        )
