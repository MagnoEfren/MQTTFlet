import flet as ft
from components.signal_generator import SignalGenerator

class GraphView:
    def __init__(self, page):
        self.page = page
        self.signal = SignalGenerator().generate()

    def go_back(self, e):
        self.page.go("/dashboard")

    def view(self):
        puntos = [ft.LineChartDataPoint(x=i, y=self.signal[i]) for i in range(len(self.signal))]

        grafica = ft.LineChart(
            data_series=[
                ft.LineChartData(
                    data_points=puntos,
                    stroke_width=4,
                    color=ft.colors.GREEN_ACCENT,
                    curved=True
                )
            ],
            tooltip_bgcolor=ft.colors.GREEN_900,
            min_y=0,
            max_y=100,
            expand=True
        )

        return ft.View(
            "/graph",
            controls=[
                ft.AppBar(
                    title=ft.Text("Gráfica Analógica"),
                    bgcolor=ft.colors.GREEN_700,
                    leading=ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=self.go_back),
                ),
                ft.Container(
                    content=grafica,
                    padding=20,
                    expand=True
                )
            ]
        )
