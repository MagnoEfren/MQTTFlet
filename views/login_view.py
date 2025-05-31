import flet as ft

class LoginView:
    def __init__(self, page, on_login_success):
        self.page = page
        self.green = "#06f998"

        self.on_login_success = on_login_success
        self.email = ft.TextField(label="Usuario", border_radius=15, on_focus=self.clear_data_band,
                                  focused_border_color=self.green, label_style=ft.TextStyle(color="white")
                                  )
        self.password = ft.TextField(label="Contraseña",border_radius=15, password=True, 
                                    can_reveal_password=True, focused_border_color= self.green,
                                    label_style=ft.TextStyle(color="white"))
        
        self.label_indicator = ft.Text(value= "Credenciales incorrectos", visible=False, color="red")

    def login(self, e):
        if self.email.value == "admin":
            if self.password.value =="1234":
                self.on_login_success()
            else:
                self.label_indicator.visible = True
                self.email.value = ""
                self.password.value = ""
        else:
            self.label_indicator.visible = True
            self.email.value = ""
            self.password.value = ""
        self.on_login_success()
        self.page.update()
    
    def clear_data_band(self, e):
        self.label_indicator.visible = False
        self.page.update()


    def view(self):
        return ft.View(
            "/",
            controls=[
                ft.Column(
                    [
                        ft.Text("SERVITEC \n PROCESS", size=30, weight="bold"),
                        self.email,
                        self.password,
                        ft.Container(
                            content=ft.Text("Ingresar", expand=True, color="black",
                                            weight="bold", size=15),
                            border_radius=15,
                            height=50,
                            on_click=self.login,
                            alignment=ft.alignment.center,
                            bgcolor=  self.green
                        ),
                        self.label_indicator,
                        
                        ft.Row(
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=0,
                            controls=[
                                ft.IconButton(icon=ft.icons.LOCK_RESET, icon_color="blue400", on_click=self.forgot_password_click,),
                                ft.Text(
                                    value="Recuperar contraseña",
                                    color="white"  
                                ),
                            ],
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,expand= True,
                )
            ],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            padding=30
        )
    


    def forgot_password_click(self, e):
        pass
