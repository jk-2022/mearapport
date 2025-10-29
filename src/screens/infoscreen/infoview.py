from flet import *
from uix.customtitlelabel import CustomTitleLabel
from utils.utilhttpx import UtilHttpx

class InfoView(View):
    def __init__(self, page:Page, **k):
        super().__init__(*k)
        self.page=page

        username,_=UtilHttpx.load_credentials()
        self.username_field=CustomTitleLabel(page=self.page, title="Numéro téléphone", value=username)
        self.email_field=CustomTitleLabel(page=self.page, title="Email", value='jeantexte19@gmail.com')
        self.btn_dem=TextButton("Je veux être demarcheur!")

        widht=(self.page.window.width-160)/2

        con_avatar=Container(
            height=120,
            alignment=alignment.center,
            content=Stack(
                controls=[
                    IconButton(icon=Icons.PERSON, icon_size=80,
                         right=widht,left=widht,top=0,bottom=0)
                ]
            )
        )
        con_fields=Container(
            height=210,
            padding=10,
            content=Column(
                expand=True,
                alignment=CrossAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    self.username_field,
                    self.email_field,
                    Row(
                            alignment=MainAxisAlignment.END,
                            controls=[
                                IconButton(icon=Icons.EDIT)
                            ]
                        ),
                ]
            )
        )
        self.controls=[
            SafeArea(
                Column(
                    expand=True,
                    controls=[
                        IconButton(icon=Icons.ARROW_BACK, data="/",
                                             on_click= self.page.on_view_pop),
                        con_avatar,
                        Card(
                            content=con_fields
                        ),
                        Row(
                            alignment=MainAxisAlignment.END,
                            controls=[
                                self.btn_dem
                            ]
                        )
                    ]
                ),
                expand=True
            )]
        
    def go_back_to_products(self,e):
        self.page.on_view_pop(e=None)
