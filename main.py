
import flet as ft
from app import IoTApp

def main(page: ft.Page):
    app = IoTApp(page)
    app.run()

ft.app(target=main)
