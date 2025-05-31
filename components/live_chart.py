# components/live_chart.py
import flet as ft
from collections import deque


def hex_with_opacity(hex_color: str, opacity: float) -> str:
    """Convierte #RRGGBB y opacidad (0-1) a formato rgba() válido"""
    hex_color = hex_color.lstrip("#")
    r, g, b = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r},{g},{b},{opacity})"


class LiveChart:
    def __init__(
        self,
        page: ft.Page,
        label_y: str = "Valor",
        color: str = "#0000FF",  # Por defecto azul en hex
        y_min: float = None,
        y_max: float = None,
        curved: bool = True,
        max_points: int = 100,
    ):
        self.page = page
        self.label_y = label_y
        self.color = color
        self.y_min = y_min
        self.y_max = y_max
        self.curved = curved
        self.max_points = max_points
        
        self.data = deque([0] * max_points, maxlen=max_points)
        initial_points = [ft.LineChartDataPoint(x=i, y=0) for i in range(max_points)]
        
        self.chart = ft.LineChart(
            data_series=[
                ft.LineChartData(
                    data_points=initial_points,
                    stroke_width=3,
                    color=self.color,
                    curved=curved,
                )
            ],
            min_y=y_min if y_min is not None else 0,
            max_y=y_max if y_max is not None else 10,
            tooltip_bgcolor="#000000",
            animate=300,
            expand=True,
            height=300,
            left_axis=ft.ChartAxis(
                title=ft.Text(label_y, size=12, weight="bold"),
                title_size=40,
                labels_size=35,
            ),
            bottom_axis=ft.ChartAxis(
                title=ft.Text("Tiempo", size=12),
                title_size=40,
                labels_size=35,
            ),
            horizontal_grid_lines=ft.ChartGridLines(
                color=hex_with_opacity("#000000", 0.2),
                width=1,
                dash_pattern=[3, 3],
            ),
            vertical_grid_lines=ft.ChartGridLines(
                color=hex_with_opacity("#000000", 0.2),
                width=1,
                dash_pattern=[3, 3],
            ),
        )
        
        self.container = ft.Container(
            padding=20,
            border_radius=20,
            bgcolor=hex_with_opacity(self.color, 0.05),
            content=ft.Column([
                ft.Text(label_y, size=18, weight="bold", color=self.color),
                self.chart
            ])
        )

    def control(self):
        return self.container

    def update_data(self, new_value: float):
        self.data.append(new_value)
        points = [ft.LineChartDataPoint(x=i, y=self.data[i]) for i in range(len(self.data))]
        
        self.chart.data_series = [
            ft.LineChartData(
                data_points=points,
                stroke_width=3,
                color=self.color,
                curved=self.curved,
            )
        ]
        
        if self.y_min is None or self.y_max is None:
            non_zero_values = [v for v in self.data if v != 0]
            if non_zero_values:
                min_val = min(non_zero_values)
                max_val = max(non_zero_values)
                padding = abs(max_val - min_val) * 0.1 if max_val != min_val else abs(max_val) * 0.1
                self.chart.min_y = min_val - padding
                self.chart.max_y = max_val + padding
            else:
                self.chart.min_y = -1
                self.chart.max_y = 1

        self.page.update()
