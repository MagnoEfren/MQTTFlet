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
                ft.ResponsiveRow(
                    #columns=2,
                    spacing=10,
                    col={"xs": 12, "sm": 6, "md": 4, "lg": 3},  # ¡Responsivo!
                    controls=[
                        
                        self.create_menu_card(ft.icons.SENSORS, "Sensores", self.go_to_sensors),
                        self.create_menu_card(ft.icons.AIR, "Motores", self.go_to_motor),
                        self.create_menu_card(ft.icons.SHOW_CHART, "Gráficas", self.go_to_graph),
                        self.create_menu_card(ft.icons.SETTINGS, "Configuraciones", self.go_to_settings),


                    ]
                )
            ]
        )

    def create_menu_card(self, icon: str, text: str, on_click_func=None):
        return ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Icon(name=icon, size=40, color="black"),
                                ft.Text(value=text, weight=ft.FontWeight.W_500, size=14),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=8,
                        ),
                        padding=ft.padding.all(16),
                        bgcolor=self.green,
                        border_radius=12,
                        on_click=on_click_func,
                        on_hover=self.on_hover_effect,
                    ),
                    col={"xs": 12, "sm": 6, "md": 4, "lg": 3},  # ¡Responsivo!
                    elevation=4  # Ahora sí funciona aquí
                )


    def on_hover_effect(self, e: ft.ControlEvent):
        e.control.bgcolor = "#00ffea" if e.data == "true" else "#05695c"
        e.control.elevation = 8 if e.data == "true" else 3
        e.control.update()
