from flet import *

class CustomTitleLabel(Container):
    def __init__(self,title,value,**kwargs):
        super().__init__()
        self.padding=5
        self.content=Row(
            [
                Container(
                    content=Text(title,height=20),
                    width=150,
                    alignment=alignment.center_left,
                    adaptive=True
                ),
                Container(
                    content=Text(':'),
                    width=20,
                    alignment=alignment.center_left,
                    adaptive=True,
                    height=20
                ),
                Container(
                    content=Row(
                        [
                            Text(value,weight=FontWeight.W_300)
                        ],alignment=MainAxisAlignment.CENTER
                    ),
                    # expand=True,
                    adaptive=True,
                )
            ],spacing=0
        )