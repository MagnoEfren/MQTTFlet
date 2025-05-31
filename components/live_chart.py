# components/live_chart.py
import flet as ft
from collections import deque


class LiveChart:
    def __init__(
        self,
        page: ft.Page,  # Agregar page como parámetro requerido
        label_y: str = "Valor",
        color: str = ft.colors.BLUE,
        y_min: float = None,
        y_max: float = None,
        curved: bool = True,
        max_points: int = 100,
    ):
        self.page = page  # Guardar referencia a la página
        self.label_y = label_y
        self.color = color
        self.y_min = y_min
        self.y_max = y_max
        self.curved = curved
        self.max_points = max_points
        
        # Inicializar con 50 valores en 0
        self.data = deque([0] * max_points, maxlen=max_points)
        
        # Crear puntos iniciales (todos en 0)
        initial_points = [ft.LineChartDataPoint(x=i, y=0) for i in range(max_points)]
        
        self.chart = ft.LineChart(
            data_series=[
                ft.LineChartData(
                    data_points=initial_points,
                    stroke_width=3,
                    color=self.color,#color de la linea
                    curved=curved,
                    
                )
            ],
            min_y=y_min if y_min is not None else 0,
            max_y=y_max if y_max is not None else 10,
            tooltip_bgcolor="black", # valor del bgcolor del indicador
            animate=300, # tiempo de actualización
            expand=True,
            height=300,
            # Configurar ejes
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
                color=ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE),
                width=1,
                dash_pattern=[3, 3],
            ),
            vertical_grid_lines=ft.ChartGridLines(
                color=ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE),
                width=1,
                dash_pattern=[3, 3],
            ),
        )
        
        self.container = ft.Container(
            padding=20,
            border_radius=20,
            bgcolor=ft.colors.with_opacity(0.05, color),
            content=ft.Column([
                ft.Text(label_y, size=18, weight="bold", color=color),
                self.chart
            ])
        )

    def control(self):
        return self.container

    def update_data(self, new_value: float):
        # Agregar el nuevo valor (esto desplaza automáticamente los datos anteriores)
        self.data.append(new_value)
        
        # Crear puntos con todos los 50 valores (incluyendo ceros iniciales)
        points = [ft.LineChartDataPoint(x=i, y=self.data[i]) for i in range(len(self.data))]
        
        # Actualizar la serie de datos
        self.chart.data_series = [
            ft.LineChartData(
                data_points=points,
                stroke_width=3,
                color=self.color,
               # below_line_bgcolor=self.color,
                curved=self.curved,
            )
        ]
        
        # Auto ajuste del rango si no se define
        if self.y_min is None or self.y_max is None:
            # Filtrar solo los valores que no sean 0 para el cálculo de rango
            non_zero_values = [v for v in self.data if v != 0]
            if non_zero_values:
                min_val = min(non_zero_values)
                max_val = max(non_zero_values)
                padding = abs(max_val - min_val) * 0.1 if max_val != min_val else abs(max_val) * 0.1
                self.chart.min_y = min_val - padding
                self.chart.max_y = max_val + padding
            else:
                # Si todos son ceros, mantener un rango por defecto
                self.chart.min_y = -1
                self.chart.max_y = 1
        
        # CRÍTICO: Actualizar la página
        self.page.update()