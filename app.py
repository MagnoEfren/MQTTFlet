from views.login_view import LoginView
from views.dashboard_view import DashboardView
from views.graph_view import GraphView
import flet as ft 

class IoTApp:
    def __init__(self, page):
        self.page = page
        self.page.title = "IoT Control App"
        self.page.theme_mode = "DARK"
        self.page.on_route_change = self.route_change

    def run(self):
        self.page.go("/")  # Esto dispara route_change

    def route_change(self, e):
        route = self.page.route

        if route == "/":
            view = LoginView(self.page, self.go_to_dashboard).view()
        elif route == "/dashboard":
            view = DashboardView(self.page).view()
        elif route == "/graph":
            view = GraphView(self.page).view()
        else:
            view = ft.View("/", [ft.Text("404 - Página no encontrada")])

        self.page.views.clear()
        self.page.views.append(view)
        self.page.update()  # <<< Esto es CRUCIAL para que se muestre
        self.page.go(route)  # <<< Refresca la ruta activa (opcional pero útil)

    def go_to_dashboard(self):
        self.page.go("/dashboard")
        
    def go_to_login(self):
        self.page.views.clear()
        self.page.go("/")

    def go_back(self):
        if len(self.page.views) > 1:
            self.page.views.pop()
            self.page.go(self.page.views[-1].route)
