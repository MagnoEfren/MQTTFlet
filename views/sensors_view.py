# views/sensors_view.py
import flet as ft
from components.mqtt_client import MQTTClient


class SensorsView:
    def __init__(self, page):
        self.page = page

        # Indicadores de progreso circular
        self.nivel_indicator = ft.ProgressRing(value=0, stroke_width=10, color=ft.colors.BLUE)
        self.caudal_indicator = ft.ProgressRing(value=0, stroke_width=10, color=ft.colors.GREEN)
        self.presion_indicator = ft.ProgressRing(value=0, stroke_width=10, color=ft.colors.RED)
        self.potenciometro_indicator = ft.ProgressRing(value=0, stroke_width=10, color=ft.colors.ORANGE)

        # Etiquetas de valor
        self.nivel_value = ft.Text("Nivel: 0")
        self.caudal_value = ft.Text("Caudal: 0")
        self.presion_value = ft.Text("Presión: 0")
        self.potenciometro_value = ft.Text("Potenciómetro: 0")

        # Estado de conexión
        self.connection_status = ft.Text("🔴 Desconectado", color=ft.colors.RED)

        # Cliente MQTT
        self.mqtt_client = MQTTClient(self.on_mqtt_data)
        self.mqtt_connected = False

    def on_mqtt_data(self, data):
        try:
            # Normalizar los valores para el progress bar entre 0 y 1
            nivel = min(float(data['n']) / 5000, 1)
            caudal = min(float(data['c']) / 100, 1)
            presion = min(float(data['p']) / 10, 1)
            potenciometro = min(float(data['o']) / 11000, 1)

            # Actualizar progress bars
            self.nivel_indicator.value = nivel
            self.caudal_indicator.value = caudal
            self.presion_indicator.value = presion
            self.potenciometro_indicator.value = potenciometro

            # Actualizar texto
            self.nivel_value.value = f"Nivel: {data['n']}"
            self.caudal_value.value = f"Caudal: {data['c']}"
            self.presion_value.value = f"Presión: {data['p']}"
            self.potenciometro_value.value = f"Potenciómetro: {data['o']}"

            self.page.update()
        except Exception as e:
            print(f"❌ Error en actualización de sensores: {e}")

    def start_mqtt_connection(self, e):
        if not self.mqtt_connected:
            success = self.mqtt_client.connect(
                broker="test.mosquitto.org",
                port=1883,
                topic="nodered/datos",
                client_id="APP_SENSORS"
            )
            if success:
                self.mqtt_connected = True
                self.connection_status.value = "🟢 Conectado"
                self.connection_status.color = ft.colors.GREEN
                e.control.text = "Detener"
                e.control.on_click = self.stop_mqtt_connection
                e.control.bgcolor = ft.colors.RED
            else:
                self.connection_status.value = "🔴 Error de conexión"
                self.connection_status.color = ft.colors.RED

            self.page.update()

    def stop_mqtt_connection(self, e):
        if self.mqtt_connected:
            self.mqtt_client.disconnect()
            self.mqtt_connected = False
            self.connection_status.value = "🔴 Desconectado"
            self.connection_status.color = ft.colors.RED
            e.control.text = "Iniciar"
            e.control.on_click = self.start_mqtt_connection
            e.control.bgcolor = ft.colors.GREEN
            self.page.update()

    def go_back(self, e):
        if self.mqtt_connected:
            self.mqtt_client.disconnect()
        self.page.go("/dashboard")

    def view(self):
        mqtt_button = ft.ElevatedButton(
            text="Iniciar",
            icon=ft.icons.PLAY_ARROW,
            bgcolor=ft.colors.GREEN,
            color=ft.colors.WHITE,
            on_click=self.start_mqtt_connection
        )

        def create_sensor_display(label, indicator, value_text):
            return ft.Column([
                ft.Text(label, size=14, weight="bold"),
                ft.Container(
                    content=indicator,
                    width=100,
                    height=100,
                    alignment=ft.alignment.center
                ),
                value_text
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        return ft.View(
            "/sensors",
            controls=[
                ft.AppBar(
                    title=ft.Text("Sensores"),
                    bgcolor=ft.colors.GREEN_700,
                    leading=ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=self.go_back),
                ),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text("MQTT:", size=12, weight="bold"),
                            self.connection_status,
                            mqtt_button
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20
                    ),
                    padding=20,
                ),
                ft.Container(
                    expand=True,
                    content=ft.GridView(
                        runs_count=2,
                        max_extent=180,
                        spacing=20,
                        controls=[
                            create_sensor_display("Nivel", self.nivel_indicator, self.nivel_value),
                            create_sensor_display("Caudal", self.caudal_indicator, self.caudal_value),
                            create_sensor_display("Presión", self.presion_indicator, self.presion_value),
                            create_sensor_display("Potenciómetro", self.potenciometro_indicator, self.potenciometro_value),
                        ]
                    ),
                    padding=20
                )
            ]
        )
