import flet as ft
from views.login_view import LoginView
from views.dashboard_view import DashboardView
from views.graph_view import GraphView
from views.sensors_view import SensorsView
from views.motor_view import MotorView
from views.settings_view import SettingsView


class IoTApp:
    def __init__(self, page):
        self.page = page
        self.page.theme_mode = "DARK"
        self.page.on_route_change = self.route_change

        #  Solo se crean UNA VEZ
        self.login_view = LoginView(self.page, self.go_to_dashboard)
        self.dashboard_view = DashboardView(self.page)
        self.graph_view = GraphView(self.page)
        self.sensors_view = SensorsView(self.page)
        self.motor_view = MotorView(self.page)
        self.settings_view = SettingsView(self.page)

    def run(self):
        self.page.go("/")  # Dispara route_change

    def route_change(self, e):
        route = self.page.route

        if route == "/":
            view = self.login_view.view()
        elif route == "/dashboard":
            view = self.dashboard_view.view()
        elif route == "/graph":
            view = self.graph_view.view()
        elif route == "/sensors":
            view = self.sensors_view.view()
        elif route == "/motor":
            view = self.motor_view.view()
        elif route == "/settings":
            view = self.settings_view.view()
        else:
            view = ft.View("/", [ft.Text("404 - Página no encontrada")])

        self.page.views.clear()
        self.page.views.append(view)
        self.page.update()

    def go_to_dashboard(self):
        self.page.go("/dashboard")

    def go_to_login(self):
        self.page.views.clear()
        self.page.go("/")

    def go_back(self):
        if len(self.page.views) > 1:
            self.page.views.pop()
            self.page.go(self.page.views[-1].route)
