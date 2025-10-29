
from flet import *
from mystorage import *

class AcceuilView(View):
    def __init__(self,page:Page,route:str="/",**k):
        super().__init__()
        self.expand=True
        self.page=page
        self.padding=0
        bar_cnt=Container(height=60,
                        #  bgcolor=Colors.BLUE_GREY,
                         
                         content=Row(
                             [
                                IconButton(icon=Icons.MENU, on_click =  self.open_drawer),
                                Text("ACTIVITE ET RAPPORT ", text_align=TextAlign.CENTER,
                                     size=24, weight=FontWeight.BOLD),
                                IconButton(icon=Icons.LIGHT_MODE, on_click=self.togle_theme)
                             ],alignment=MainAxisAlignment.SPACE_BETWEEN
                            )
                         )
        
        self.drawer = NavigationDrawer(
        # on_dismiss=handle_dismissal,
        on_change=self.handle_change,
        controls=[
                Container(
                    height=120,
                    content=CircleAvatar(content=Icon(name=Icons.PERSON)),
                    padding=10
                ),
                Divider(thickness=2),
                Column(
                    [
                        Container(
                            content=Column([
                                    ListTile(title=Text("A propos"),leading=Icon(name=Icons.INFO), on_click=self.go_apropos),
                                    ListTile(title=Text("Archives"),leading=Icon(name=Icons.ARCHIVE),on_click=self.go_archive),
                                    ListTile(title=Text("Paramètres"),leading=Icon(name=Icons.SETTINGS),on_click=self.go_settings),
                                        ]
                            ),
                                ),
                        Divider(thickness=2),
                        Row(
                            [
                                Text("jeankolou19@gmail.com\nTel:90007727")
                            ],alignment=MainAxisAlignment.CENTER,
                        ),
                        Container(
                            content=TextButton('Nous contacter !'),
                        ),
                    ],
                    expand=1,
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    horizontal_alignment=CrossAxisAlignment.END,
                )
            ],
        )
        
        self.controls.append(SafeArea(
            Stack(
                controls=[

                    Image(
                        src="eau2.png",
                        width=page.width,
                        height=page.height,
                        fit=ImageFit.COVER,
                    ),
                    
                    Container(
                        content=Column(
                                    [
                                        ElevatedButton(" 📋  RAPPORT D'ACTIVITE  ", on_click=self.page_go_project, elevation=10),
                                        # ElevatedButton(" 📁  LISTE DES OUVRAGES  ", on_click=self.page_go_list_ouvrage, elevation=10),
                                    ],
                                    expand=True,
                                    alignment=MainAxisAlignment.CENTER,
                                    spacing=40
                                ),
                            alignment=alignment.center,
                            expand=True,
                            top=0,bottom=0,left=0,right=0
                            ),
                    bar_cnt



                ]
            )
                )
            )
        
    def go_apropos(self,e):
        self.handle_change(e=None)
        self.page.go("/apropos")
    
    def open_drawer(self,e):
        self.page.open(self.drawer)
        
    def handle_change(self,e):
        # print(f"Selected Index changed: {e.control.selected_index}")
        self.page.close(self.drawer)
 
    def page_go_project(self,e):
        self.page.go('/project')
    
    def go_archive(self,e):
        self.handle_change(e=None)
        self.page.go('/archive')
    
    def go_settings(self,e):
        self.handle_change(e=None)
        self.page.go('/settings')

    def togle_theme(self,e):
        if self.page.theme_mode == ThemeMode.DARK : 
            self.page.theme_mode=ThemeMode.LIGHT
            set_value('theme','ThemeMode.LIGHT')
        else:
            self.page.theme_mode=ThemeMode.DARK
            set_value('theme','ThemeMode.DARK')
        self.page.update()

    def page_go_list_ouvrage(self,e):
        self.page.go('/list-ouvrage')