from flet import *
from donnees import *
from myaction import get_all_communes, get_stats_commune
from .statanneecommunecontrol import StatAnneeCommuneControl
from .statcommunecontrol import StatCommuneControl


class StatCommuneView(View):
    def __init__(self, page : Page,route:str="/statcommune"):
        super().__init__()
        self.page=page
        
        self.commune = Dropdown(label="Voir stat par commune", options=[
        ],expand=True,border_color=Colors.WHITE54 if self.page.theme_mode==ThemeMode.DARK else Colors.BLACK38,
        on_change=self.show_tab_stat_by_commune)
        list_commune = get_all_communes() 
        
        for key in list_commune:
            self.commune.options.append(dropdown.Option(key))
        
        self.commune_res_cont=Column(expand=True, scroll=ScrollMode.ALWAYS)
        
        self.controls.append(
            SafeArea(
                Column(
                    controls=[
                        Row(
                            [
                            IconButton(icon=Icons.ARROW_BACK,on_click=self.page.on_view_pop),
                            Text(f"📁 Stastistiques par Communes")
                            ]
                        ),
                        self.commune,
                        self.commune_res_cont
                    
                    ],
                    expand=True,
                    scroll=ScrollMode.ALWAYS
                )
                ,expand=True
            )
        )
        
    def show_tab_stat_by_commune(self,e):
        commune=e.control.value
        stats=get_stats_commune(commune)
        cont_commune=StatCommuneControl(commune=commune, stat_general=stats)
        cont_commune_annee=StatAnneeCommuneControl(page=self.page, stat_general=stats)

        self.commune_res_cont.controls.clear()
        self.commune_res_cont.controls.append(cont_commune)
        self.commune_res_cont.controls.append(cont_commune_annee)
        self.commune_res_cont.update()
        
