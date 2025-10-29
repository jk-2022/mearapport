# import os
from flet import *

from uix.customtitlelabel import CustomTitleLabel

from .datatablestat import Mytable_ouvrage, tb_ouvrage

class TableCommune(Container):
    def __init__(self,page:Page, commune, stats):
        super().__init__()
        self.page=page
        self.tab_cnt_general=Column()
        self.elevation=5
        self.stats=stats
        self.commune=commune

        self.content=Container(
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
                ))
        tb_ouvrage.rows=[]
        self.tab_cnt_general.controls.clear()
        # print(stats)
        stat_commune=stats['par_type']
        for types in stat_commune.keys():
            tb_ouvrage.rows.append(
                        DataRow(
                            cells=[
                                DataCell(Text(types)),
                                DataCell(Text(stat_commune[types]['Bon état'])),
                                DataCell(Text(stat_commune[types]['Panne'])),
                                DataCell(Text(stat_commune[types]['Abandonné'])),
                                DataCell(Text(stat_commune[types]['total_ouvrage'])),
                            ]
                        )
                    )
            cont=Column(
                [
                    Row(
                        [
                            Container(
                                content=Text(f"{self.commune}")
                            )
                        ],alignment=MainAxisAlignment.CENTER,
                    
                    ),
                    Column(
                        [
                            CustomTitleLabel(title="Nombre en état",value=self.stats['total_bon_etat']),
                            CustomTitleLabel(title="Nombre en panne",value=self.stats['total_panne']),
                            CustomTitleLabel(title="Nombre Abandonné",value=self.stats['total_abandonne']),
                            CustomTitleLabel(title="Nombre d'ouvrages",value=self.stats['total_ouvrages'])
                        ],spacing=0
                    ),
                    Mytable_ouvrage
                ]
            )
        self.tab_cnt_general.controls.append(cont)
    
   

