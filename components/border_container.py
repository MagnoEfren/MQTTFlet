import flet as ft

class BorderedContainer(ft.Container):
    def __init__(self, content, padding=10, border_color=ft.colors.GREY_800, radius=10):
        super().__init__(
            content=content,
            padding=padding,
            border=ft.border.all(1, border_color),
            border_radius=radius,
        )
