from flet import *

from donnees import *
from myaction import get_all_cantons, get_stats_canton
from .statanneecantoncontrol import StatAnneeCantonControl
from .statcantoncontrol import StatCantonControl

class StatCantonView(View):
    def __init__(self, page : Page,route:str="/statcanton"):
        super().__init__()
        self.page=page
        
        self.canton = Dropdown(label="Voir stat par canton", options=[
        ],expand=True,border_color=Colors.WHITE54 if self.page.theme_mode==ThemeMode.DARK else Colors.BLACK38,
        on_change=self.show_tab_stat_by_canton)
        self.list_cantons = get_all_cantons()
       
        for key in self.list_cantons:
            self.canton.options.append(dropdown.Option(key))
            
        self.canton_res_cont=Column(expand=True, scroll=ScrollMode.ALWAYS)
        
        self.controls.append(
            SafeArea(
                Column(
                    controls=[
                        Row(
                            [
                            IconButton(icon=Icons.ARROW_BACK,on_click=self.page.on_view_pop),
                            Text(f"📁 Stastistiques par Canton")
                            ]
                        ),
                        self.canton,
                         self.canton_res_cont
                    
                    ],
                    expand=True,
                    scroll=ScrollMode.ALWAYS
                )
                ,expand=True
            )
        )
    def show_tab_stat_by_canton(self,e):
        canton=e.control.value
        stats=get_stats_canton(canton)
        print(stats)
        cont_canton=StatCantonControl(canton=canton, stat_general=stats)
        cont_canton_annee=StatAnneeCantonControl(page=self.page, stat_general=stats)

        self.canton_res_cont.controls.clear()
        self.canton_res_cont.controls.append(cont_canton)
        self.canton_res_cont.controls.append(cont_canton_annee)
        self.canton_res_cont.update()
        
