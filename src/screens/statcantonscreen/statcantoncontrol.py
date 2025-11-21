# import os

from flet import *

from uix.customtitlelabel import CustomTitleLabel
# from screens.staticscreen.tablecanton import TableCanton
from .datatablestat import Mytable_ouvrage, tb_ouvrage

class StatCantonControl(Card):
    def __init__(self, canton, stat_general):
        super().__init__()
        self.tab_cnt_general=Column( expand=True )
        self.elevation=5
        self.stat_general=stat_general
        self.content=Container(
            # on_click=lambda e: self.selectprojet(e),
            padding=padding.all(10),
            expand=True,
            content=Column(
                        [
                            Row(
                                [
                                    Container(
                                        content=Text(f"Statsistiques pour", size=11, italic=True),alignment=alignment.center
                                    )
                                ],alignment=MainAxisAlignment.CENTER
                            ),
                            self.tab_cnt_general,
                        ]
                    )
                )
        
        stat_canton=stat_general['par_type']
        tb_ouvrage.rows=[]
        for types in stat_canton.keys():
            tb_ouvrage.rows.append(
                        DataRow(
                            cells=[
                                DataCell(Text(types)),
                                DataCell(Text(stat_canton[types]['Bon état'])),
                                DataCell(Text(stat_canton[types]['En panne'])),
                                DataCell(Text(stat_canton[types]['Abandonné'])),
                                DataCell(Text(stat_canton[types]['total_ouvrage'])),
                            ]
                        )
                    )
            cont=Column(
                [
                    Row(
                        [
                            Container(
                                content=Text(f"{canton}")
                            )
                        ],alignment=MainAxisAlignment.CENTER,
                    
                    ),
                    Column(
                        [
                            CustomTitleLabel(title="Nombre en état",value=stat_general['total_bon_etat']),
                            CustomTitleLabel(title="Nombre en panne",value=stat_general['total_panne']),
                            CustomTitleLabel(title="Nombre Abandonné",value=stat_general['total_abandonne']),
                            CustomTitleLabel(title="Nombre d'ouvrages",value=stat_general['total_ouvrages'])
                        ],spacing=0
                    ),
                    Mytable_ouvrage
                ]
            )
        self.tab_cnt_general.controls.append(cont)
        # stat_canton={}
