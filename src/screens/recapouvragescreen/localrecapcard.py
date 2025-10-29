import os
import sqlite3
from flet import *

from myaction import load_all_data
from uix.customtitlelabel import CustomTitleLabel

from allpath import AllPath
path=AllPath()
path_data=path.path_data()

DB_PATH=os.path.join(path_data,"rapport.db")
ARCHIVES_PATH=path.path_generated_docs()


class LocalRecapCard(Card):
    def __init__(self, page: Page, donnees):
        super().__init__()
        self.page=page
        self.donnees=donnees
        self.elevation=5
        self.cont=Column( spacing=0)
        # print(self.donnees)
        self.cont.controls.clear()
        if donnees:
            list_item=['id','projet_id','localisation_id','created_at']
            for key, val in donnees.items():
                if key in list_item or val=="" or val==None:
                    pass 
                else:
                    self.cont.controls.append(
                        CustomTitleLabel(title=key,value=val))
        else:
            self.cont.controls.append(Row(
                [
                    Text("Pas de données de Localisation enrégistré")
                ],alignment=MainAxisAlignment.CENTER))
        try:
            self.cont.update()
        except:
            pass

        self.content=Container(
            border_radius=10,
            border=border.all(1,Colors.YELLOW_500),
            expand=True,
            content=Column(
                [
                    Row(
                        [
                            Text("Localisation",text_align=TextAlign.CENTER,color=Colors.YELLOW_500)
                        ],alignment=MainAxisAlignment.CENTER
                    ),
                    self.cont,
                    Row(
                        [
                            ElevatedButton('Maps',icon=Icons.MAP,icon_color=Colors.GREEN_500,on_click=""),
                        ]
                        # ,alignment=MainAxisAlignment.SPACE_EVENLY
                    )
                ]
            )
        )


 


    