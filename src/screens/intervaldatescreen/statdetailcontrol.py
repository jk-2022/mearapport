# import os

from flet import *

from .datatablestat import Mytable_detail_ouvrage, tb_detail_ouvrage

class StatDetailControl(Card):
    def __init__(self, stats_data):
        super().__init__()
        self.tab_cnt_general=Column( expand=True, scroll=ScrollMode.ALWAYS )
        self.elevation=5
        self.stats_data=stats_data
        self.content=Container(
            padding=padding.all(10),
            expand=True,
            content=Column(
                        [   
                            self.tab_cnt_general,
                        ]
                    )
                )
        
        tb_detail_ouvrage.rows=[]
        for ouvrage in stats_data:
            tb_detail_ouvrage.rows.append(
                        DataRow(
                            cells=[
                                DataCell(Text(ouvrage['type_ouvrage'])),
                                DataCell(Text(ouvrage['lieu'])),
                                DataCell(Text(ouvrage['canton'])),
                                DataCell(Text(ouvrage['commune'])),
                                DataCell(Text(ouvrage['etat'])),
                                DataCell(Text(ouvrage['annee'])),
                            ]
                        )
                    )
            cont=Column(
                [
                    Row(
                        [
                            Container(
                                content=Text(f"Listes des ouvrages")
                            )
                        ],alignment=MainAxisAlignment.CENTER,
                    
                    ),
                    Mytable_detail_ouvrage
                ]
            )
        self.tab_cnt_general.controls.append(cont)
        # stat_commune={}
