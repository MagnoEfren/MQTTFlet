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
        
        # Crear los gráficos para cada variable
        self.chart_nivel = LiveChart(
            page=page,
            label_y="Nivel", 
            color=ft.colors.BLUE,
            y_min=0,
            y_max=5000  # Ajustar según tus datos reales
        )
        
        self.chart_caudal = LiveChart(
            page=page,
            label_y="Caudal", 
            color=ft.colors.GREEN, 
            y_min=0, 
            y_max=100  # Ajustar según tus datos reales
        )
        
        self.chart_presion = LiveChart(
            page=page,
            label_y="Presión", 
            color=ft.colors.RED,
            y_min=0,
            y_max=10  # Ajustar según tus datos reales
        )
        
        self.chart_potenciometro = LiveChart(
            page=page,
            label_y="Potenciómetro", 
            color=ft.colors.ORANGE,
            y_min=0,
            y_max=11000  # Ajustar según tus datos reales
        )
        
        # Cliente MQTT
        self.mqtt_client = MQTTClient(self.on_mqtt_data)
        self.mqtt_connected = False
        
        # Control de conexión
        self.connection_status = ft.Text("🔴 Desconectado", color=ft.colors.RED)

    def on_mqtt_data(self, data):
        """Callback que recibe los datos del MQTT y actualiza los gráficos"""
        try:
            # Actualizar cada gráfico con su respectivo dato
            self.chart_nivel.update_data(float(data['n']))       # nivel
            self.chart_caudal.update_data(float(data['c']))      # caudal  
            self.chart_presion.update_data(float(data['p']))     # presión
            self.chart_potenciometro.update_data(float(data['o'])) # potenciómetro
            
            print(f"📊 Datos graficados - N:{data['n']}, C:{data['c']}, P:{data['p']}, O:{data['o']}, 1111111111111111111111111")
           # time.sleep(1)
            self.page.update()
        except Exception as e:
            print(f"❌ Error actualizando gráficos: {e}")
        

    def start_mqtt_connection(self, e):
        """Iniciar conexión MQTT"""
        if not self.mqtt_connected:
            # Aquí configuras tus parámetros del broker
            broker = "test.mosquitto.org"  # Cambiar por tu broker
            port = 1883               # Cambiar por tu puerto
            topic = "nodered/datos"        # Cambiar por tu topic
            client_id = "APP FLET"
            username = ""   # Opcional
            password = ""  # Opcional
            
            # Intentar conectar
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
                self.connection_status.color = ft.colors.GREEN
                e.control.text = "Detener"
                e.control.on_click = self.stop_mqtt_connection
                e.control.bgcolor = ft.colors.RED
            else:
                self.connection_status.value = "🔴 Error de conexión"
                self.connection_status.color = ft.colors.RED
                
            self.page.update()

    def stop_mqtt_connection(self, e):
        """Detener conexión MQTT"""
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
        # Detener conexión MQTT al salir
        if self.mqtt_connected:
            self.mqtt_client.disconnect()
        self.page.go("/dashboard")

    def view(self):
        # Botón de control MQTT
        mqtt_button = ft.ElevatedButton(
            "Iniciar",
            icon=ft.icons.PLAY_ARROW,
            on_click=self.start_mqtt_connection,
            bgcolor=ft.colors.GREEN,
            color=ft.colors.WHITE
        )

        return ft.View(
            "/graph",
            controls=[
                ft.AppBar(
                    title=ft.Text("Monitoreo en Tiempo Real"),
                    bgcolor=ft.colors.GREEN_700,
                    leading=ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=self.go_back),
                ),
                
                # Panel de control
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
                    bgcolor=ft.colors.with_opacity(0.1, ft.colors.BLUE_GREY),
                    border_radius=10,
                    margin=ft.margin.all(10)
                ),
                
                # Gráficos en grid 2x2
                ft.Container(
                    content=ft.Column(
                        scroll="auto",
                        controls=[
                        # Primera fila
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
                    ], expand=True),
                    expand=True,
                    padding=10
                ),
            ]
        )