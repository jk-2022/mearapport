from flet import *
from myaction import get_statistiques, get_stats_commune, get_stats_canton

from mystorage import *
from donnees import *

class StatView(View):
    def __init__(self, page : Page,route:str="/stats"):
        super().__init__()
        self.page=page
        
        self.controls.append(
            SafeArea(
                Column(
                    controls=[
                        Row(
                            [
                            IconButton(icon=Icons.ARROW_BACK,on_click=self.page.on_view_pop),
                            Text(f"📁 Stastistiques")
                            ]
                        ),
                        
                        Container(
                            expand=True,
                            alignment=alignment.center,
                            # bgcolor='yellow',
                            height=self.page.window.height-110,
                            content=Column(
                                    [
                                        ElevatedButton('Stats générals', on_click=self.page_go_general),
                                        ElevatedButton('Stats communes', on_click=self.page_go_commune),
                                        ElevatedButton('Stats cantons', on_click=self.page_go_canton),
                                    ], alignment=MainAxisAlignment.SPACE_EVENLY
                                )
                        )
                        
                    ],
                    expand=True,
                    scroll=ScrollMode.ALWAYS
                )
                ,expand=True
            )
        )
        
        
        # stats_com = get_stats_commune('Oti 1')
        # stats_cam = get_stats_canton('Mogou')
        
    def page_go_general(self,e):
        stats_gen = get_statistiques()
        set_value('stats_gen', stats_gen)
        self.page.go('/statgeneral')
    def page_go_commune(self,e):
        self.page.go('/statcommune') 
    def page_go_canton(self,e):
        self.page.go('/statcanton')
        
