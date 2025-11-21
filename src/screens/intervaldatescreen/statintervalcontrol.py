# import os

from flet import *

from uix.customtitlelabel import CustomTitleLabel
# from screens.staticscreen.tablecommune import TableCommune
from .datatablestat import Mytable_ouvrage, tb_ouvrage

class StatIntervalControl(Card):
    def __init__(self, stats_data):
        super().__init__()
        self.tab_cnt_general=Column( expand=True, scroll=ScrollMode.ALWAYS )
        self.elevation=5
        self.stats_data=stats_data
        self.content=Container(
            # on_click=lambda e: self.selectprojet(e),
            padding=padding.all(10),
            expand=True,
            content=Column(
                        [   Row(
                                [
                                    Container(
                                        content=Text(f"Statsistiques par intervalle de date", size=11, italic=True),alignment=alignment.center
                                    )
                                ],alignment=MainAxisAlignment.CENTER
                            ),
                            self.tab_cnt_general,
                        ]
                    )
                )
        
        stats=stats_data['par_type_global']['par_type']
        stats_commune=stats_data['par_commune']
        texte_commune=''
        for commune in stats_commune.keys():
            texte_commune+=f"{commune}/"
        texte_commune=texte_commune[:-1]
    
        stats_canton=stats_data['par_canton']
        texte_canton=''
        for canton in stats_canton.keys():
            texte_canton+=f"{canton}/"
        texte_canton=texte_canton[:-1]
        
        tb_ouvrage.rows=[]
        for types in stats.keys():
            tb_ouvrage.rows.append(
                        DataRow(
                            cells=[
                                DataCell(Text(types)),
                                DataCell(Text(stats[types]['Bon état'])),
                                DataCell(Text(stats[types]['En panne'])),
                                DataCell(Text(stats[types]['Abandonné'])),
                                DataCell(Text(stats[types]['Total'])),
                            ]
                        )
                    )
            cont=Column(
                [
                    Row(
                        [
                            Container(
                                content=Text(f"les dates")
                            )
                        ],alignment=MainAxisAlignment.CENTER,
                    
                    ),
                    Column(
                        [
                            CustomTitleLabel(title="Total Ouvrages",value=stats_data['total_ouvrages']),
                            CustomTitleLabel(title="Total Communes",value=stats_data['total_communes']),
                            CustomTitleLabel(title="Total Cantons",value=stats_data['total_cantons']),
                            CustomTitleLabel(title="Liste Communes",value=texte_commune),
                            CustomTitleLabel(title="Liste Cantons",value=texte_canton),
                        ],spacing=0
                    ),
                    Mytable_ouvrage
                ]
            )
        self.tab_cnt_general.controls.append(cont)
        # stat_commune={}
