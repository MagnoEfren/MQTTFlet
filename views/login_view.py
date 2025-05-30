import flet as ft

class LoginView:
    def __init__(self, page, on_login_success):
        self.page = page
        self.on_login_success = on_login_success
        self.email = ft.TextField(label="Email", width=300)
        self.password = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300)

    def login(self, e):
        if self.email.value and self.password.value:
            self.on_login_success()

    def view(self):
        return ft.View(
            "/",
            controls=[
                ft.Column(
                    [
                        ft.Text("IoT Control App", size=30, weight=ft.FontWeight.BOLD),
                        self.email,
                        self.password,
                        ft.ElevatedButton("Iniciar sesión", on_click=self.login)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            ],
            vertical_alignment=ft.MainAxisAlignment.CENTER
        )
