# views/graph_view.py
import flet as ft
from components.signal_generator import SignalGenerator
from components.live_chart import LiveChart
from components.mqtt_client import MQTTClient
import random
import threading
import time


class GraphView:
    def __init__(self, page):
        self.page = page

        # Crear los gráficos para cada variable con colores en hexadecimal
        self.chart_nivel = LiveChart(
            page=page,
            label_y="Nivel",
            color="#2196F3",  # Azul
            y_min=0,
            y_max=5000
        )

        self.chart_caudal = LiveChart(
            page=page,
            label_y="Caudal",
            color="#4CAF50",  # Verde
            y_min=0,
            y_max=100
        )

        self.chart_presion = LiveChart(
            page=page,
            label_y="Presión",
            color="#F44336",  # Rojo
            y_min=0,
            y_max=10
        )

        self.chart_potenciometro = LiveChart(
            page=page,
            label_y="Potenciómetro",
            color="#FF9800",  # Naranja
            y_min=0,
            y_max=11000
        )

        # Cliente MQTT
        self.mqtt_client = MQTTClient(self.on_mqtt_data)
        self.mqtt_connected = False

        # Control de conexión
        self.connection_status = ft.Text("🔴 Desconectado", color="#F44336")  # Rojo

    def on_mqtt_data(self, data):
        """Callback que recibe los datos del MQTT y actualiza los gráficos"""
        try:
            self.chart_nivel.update_data(float(data['n']))
            self.chart_caudal.update_data(float(data['c']))
            self.chart_presion.update_data(float(data['p']))
            self.chart_potenciometro.update_data(float(data['o']))

            print(f"📊 Datos graficados - N:{data['n']}, C:{data['c']}, P:{data['p']}, O:{data['o']}")
            self.page.update()
        except Exception as e:
            print(f"❌ Error actualizando gráficos: {e}")

    def start_mqtt_connection(self, e):
        """Iniciar conexión MQTT"""
        if not self.mqtt_connected:
            broker = "test.mosquitto.org"
            port = 1883
            topic = "nodered/datos"
            client_id = "APP FLET"
            username = ""
            password = ""

            success = self.mqtt_client.connect(
                broker=broker,
                port=port,
                topic=topic,
                client_id=client_id,
                username=username,
                password=password,
                tls=False
            )

            if success:
                self.mqtt_connected = True
                self.connection_status.value = "🟢 Conectado"
                self.connection_status.color = "#4CAF50"  # Verde
                e.control.text = "Detener"
                e.control.on_click = self.stop_mqtt_connection
                e.control.bgcolor = "#F44336"  # Rojo
            else:
                self.connection_status.value = "🔴 Error de conexión"
                self.connection_status.color = "#F44336"

            self.page.update()

    def stop_mqtt_connection(self, e):
        """Detener conexión MQTT"""
        if self.mqtt_connected:
            self.mqtt_client.disconnect()
            self.mqtt_connected = False
            self.connection_status.value = "🔴 Desconectado"
            self.connection_status.color = "#F44336"
            e.control.text = "Iniciar"
            e.control.on_click = self.start_mqtt_connection
            e.control.bgcolor = "#4CAF50"  # Verde
            self.page.update()

    def go_back(self, e):
        if self.mqtt_connected:
            self.mqtt_client.disconnect()
        self.page.go("/dashboard")

    def view(self):
        mqtt_button = ft.ElevatedButton(
            "Iniciar",
            icon=ft.icons.PLAY_ARROW,
            on_click=self.start_mqtt_connection,
            bgcolor="#4CAF50",  # Verde
            color="#FFFFFF"     # Blanco
        )

        return ft.View(
            "/graph",
            controls=[
                ft.AppBar(
                    title=ft.Text("Monitoreo en Tiempo Real"),
                    bgcolor="#388E3C",  # Verde más oscuro
                    leading=ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=self.go_back),
                ),

                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text("MQTT:", size=12, weight="bold"),
                            self.connection_status,
                            mqtt_button,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20
                    ),
                    padding=ft.padding.all(20),
                    bgcolor="rgba(128,128,128,0.1)",  # gris translúcido
                    border_radius=10,
                    margin=ft.margin.all(10)
                ),

                ft.Container(
                    content=ft.Column(
                        scroll="auto",
                        controls=[
                            ft.Container(
                                content=self.chart_nivel.control(),
                                expand=True,
                                padding=5
                            ),
                            ft.Container(
                                content=self.chart_caudal.control(),
                                expand=True,
                                padding=5
                            ),
                            ft.Container(
                                content=self.chart_presion.control(),
                                expand=True,
                                padding=5
                            ),
                            ft.Container(
                                content=self.chart_potenciometro.control(),
                                expand=True,
                                padding=5
                            ),
                        ],
                        expand=True
                    ),
                    expand=True,
                    padding=10
                ),
            ]
        )
