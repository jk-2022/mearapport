from flet import *

class StatBtnCard(Card):
    def __init__(self, title: str, on_click):
        super().__init__()
        self.height=60
        self.elevation=10
        self.on_click=on_click
        self.content=Container(
            content=Row(
                [
                    Text(f"{title}", size=13)
                ],alignment=MainAxisAlignment.CENTER
            ),
            ink=True,
            on_click=self.on_click,
            border_radius=10
        )



