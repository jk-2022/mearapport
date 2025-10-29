from flet import *
from myaction import get_stat_commune, get_statistiques, get_stats_canton
from screens.staticscreen.statanneecantoncontrol import StatAnneeCantonControl
from screens.staticscreen.statanneecommunecontrol import StatAnneeCommuneControl
from screens.staticscreen.statanneecontrol import StatAnneeControl
from screens.staticscreen.statcantoncontrol import StatCantonControl
from screens.staticscreen.statcommunecontrol import StatCommuneControl
from screens.staticscreen.statgeneralcontrol import StatGeneralControl
# from .datatablestat import Mytable_commune, tb_commune

from donnees import *

class StaticView(View):
    def __init__(self, page : Page,route:str="/statics"):
        super().__init__()
        self.page=page

        self.commune = Dropdown(label="Voir stat par commune", options=[
        ],expand=True,border_color=Colors.WHITE54 if self.page.theme_mode==ThemeMode.DARK else Colors.BLACK38,
        on_change=self.show_tab_stat_by_commune)
        stats_gen_and_comm = get_stat_commune() #la fonction renvoie tout en générale
        self.stats_com=stats_gen_and_comm['par_commune']
        for key in self.stats_com.keys():
            self.commune.options.append(dropdown.Option(key))
        
        self.canton = Dropdown(label="Voir stat par canton", options=[
        ],expand=True,border_color=Colors.WHITE54 if self.page.theme_mode==ThemeMode.DARK else Colors.BLACK38,
        on_change=self.show_tab_stat_by_canton)
        self.stats_canton = get_stats_canton() #la fonction renvoie tout en générale
        self.stats_can=self.stats_canton
        for key in self.stats_canton.keys():
            self.canton.options.append(dropdown.Option(key))
            
        self.general_cnt=Column()
        self.commune_res_cont=Column()
        self.commune_res_annee_cont=Column()
        self.commune_cnt=Column(
            [
                Container(height=20),
                self.commune,
                self.commune_res_cont,
                self.commune_res_annee_cont,
            ],spacing=0
        )

        self.canton_res_cont=Column()
        self.canton_res_annee_cont=Column()
        self.canton_cnt=Column(
            [
                Container(height=20),
                self.canton,
                self.canton_res_cont,
                self.canton_res_annee_cont,
            ],spacing=0
        )


        self.tabs_cont=Tabs(
            tabs=[
                Tab(
                    text="Stats général",
                    content=self.general_cnt
                ),
                Tab(
                    text="Stats par commune",
                    content=self.commune_cnt
                ),
                Tab(
                    text="Stats par canton",
                    content=self.canton_cnt
                )
            ]
        )

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
                        self.tabs_cont
                    ],
                    expand=True,
                    scroll=ScrollMode.ALWAYS
                )
                ,expand=True
            )
        )
        self.get_stat()

    def get_stat(self):
        stats_gen = get_statistiques()
        if stats_gen:
            cont_gen=StatGeneralControl(page=self.page, stat_general=stats_gen)
            cont_ann=StatAnneeControl(page=self.page, stat_general=stats_gen)
            self.general_cnt.controls.clear()
            self.general_cnt.controls.append(cont_gen)
            self.general_cnt.controls.append(cont_ann)
    
    def show_tab_stat_by_commune(self,e):
        commune=e.control.value
        stats=self.stats_com[commune]
        cont_commune=StatCommuneControl(commune=commune, stat_general=stats)
        cont_commune_annee=StatAnneeCommuneControl(page=self.page, stat_general=stats)

        self.commune_res_cont.controls.clear()
        self.commune_res_cont.controls.append(cont_commune)
        self.commune_res_cont.controls.append(cont_commune_annee)
        self.commune_res_cont.update()

    def show_tab_stat_by_canton(self,e):
        canton=e.control.value
        stats=self.stats_can[canton]
        cont_canton=StatCantonControl(canton=canton, stat_general=stats)
        cont_canton_annee=StatAnneeCantonControl(page=self.page, stat_general=stats)

        self.canton_res_cont.controls.clear()
        self.canton_res_cont.controls.append(cont_canton)
        self.canton_res_cont.controls.append(cont_canton_annee)
        self.canton_res_cont.update()
        
