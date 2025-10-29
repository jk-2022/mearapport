from typing import Any, List, Optional
from flet import *

import sqlite3
import os

from allpath import AllPath
path=AllPath()
path_data=path.path_data()
DB_PATH=os.path.join(path_data,"rapport.db")

# import json
from myaction import recuperer_liste_projets

from uix.custominputfield import CustomInputField

class ProjetUpdateForm(Container):
    def __init__(self, page: Page, projet, formcontrol):
        super().__init__()
        self.padding = 0
        self.page=page
        self.projet=projet
        self.formcontrol=formcontrol
        self.date = Text(f"{projet['created_at']}")
        self.name = CustomInputField(title="Nom projet")
        self.name.value=projet["name"]
        self.title = CustomInputField(title="Titre projet")
        self.title.value=projet["title"]


        self.content = Card(
            elevation=20,
            content=Container(
                padding=15,
                expand=True,
                content=Column(
                    scroll="always",
                    spacing=10,
                    controls=[
                        Row(
                            controls=[
                                self.date
                            ]
                        ),
                        Row(
                            controls=[
                                self.name,
                            ]
                        ),
                        self.title,
                    ]
                )
            )
        )


    def recupererDonnees(self):
        date = self.date.value
        name = self.name.value
        title = self.title.value
        return {"name": name, "title": title, "created_at": date}
        
    def SaveData(self, e):
        donnees = self.recupererDonnees()
        pid=self.projet['id']
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        try:
            c = conn.cursor()
            c.execute("UPDATE projets SET name=?, title=? WHERE id=?", (donnees["name"], donnees["title"], pid))
            conn.commit()
        except Exception as e:
            print(e)
            return False
        self.formcontrol.formcontrol.load_projects()
        self.formcontrol.close_dlg(e=None)


