# import os
from flet import *
# import sqlite3

# from allpath import AllPath
from uix.customtitlelabel import CustomTitleLabel
from .datatablestat import Mytable_ouvrage, tb_ouvrage, Mytable_annee, tb_annee



class StatGeneralControl(Card):
    def __init__(self,page:Page, stat_general):
        super().__init__()
        self.page=page
        self.tab_cnt_general=Column()
        self.elevation=5
        self.stat_general=stat_general

        self.content=Container(
            padding=padding.all(10),
            content=Column(
                [
                    Row(
                        [
                            Container(
                                content=Text(f"Statistiques générale", size=11, italic=True),alignment=alignment.center
                        )
                        ],alignment=MainAxisAlignment.CENTER
                    ),
                    Column(
                        [
                            CustomTitleLabel(title="Nombre de Projet",value=stat_general['nombre_projet']),
                            CustomTitleLabel(title="Nombre de commune",value=stat_general['nombre_commune']),
                            CustomTitleLabel(title="Nombre de canton",value=stat_general['nombre_canton']),
                            CustomTitleLabel(title="Nombre en état",value=stat_general['total_bon_etat']),
                            CustomTitleLabel(title="Nombre en panne",value=stat_general['total_panne']),
                            CustomTitleLabel(title="Nombre Abandonné",value=stat_general['total_abandonne']),
                            CustomTitleLabel(title="Nombre d'ouvrages",value=stat_general['total_ouvrages']),
                        ],spacing=0
                    ),
                    self.tab_cnt_general,
                    ]
                ))
        tb_ouvrage.rows=[]
        self.tab_cnt_general.controls.clear()
        for types in stat_general['par_type'].keys():
            tb_ouvrage.rows.append(
                        DataRow(
                            cells=[
                                DataCell(Text(types)),
                                DataCell(Text(stat_general['par_type'][types]['Bon état'])),
                                DataCell(Text(stat_general['par_type'][types]['Panne'])),
                                DataCell(Text(stat_general['par_type'][types]['Abandonné'])),
                                DataCell(Text(stat_general['par_type'][types]['total_ouvrage'])),
                            ]
                        )
                    )
        self.tab_cnt_general.controls.append(Mytable_ouvrage)
    
   

