
from flet import *

from datetime import datetime
import sqlite3
import os

from allpath import AllPath
path=AllPath()
path_data=path.path_data()
DB_PATH=os.path.join(path_data,"rapport.db")

# import json
from myaction import recuperer_liste_projets
from uix.custominputfield import CustomInputField
# from uix.customdropdown import CustomDropDown

class ProjetForm(Container):
    def __init__(self, page: Page, formcontrol):
        super().__init__()
        self.padding = 0
        self.page=page
        self.width=450
        self.formcontrol=formcontrol
        dateTime = datetime.now().strftime("%d/%m/%Y")
        self.date = Text(f"{dateTime}", height=40)
        self.name = CustomInputField(title="Nom projet")
        self.title = CustomInputField(title="Titre projet")
        self.content = Card(
            elevation=10,
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
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        try:
            c = conn.cursor()
            c.execute("""
                        INSERT INTO projets(name, title, created_at) VALUES(?,?,?)
                        """, (donnees["name"], donnees["title"],  donnees["created_at"]))
            conn.commit()
            # list_projet=recuperer_liste_projets()
            # self.page.data['projets']=list_projet
        except Exception as e:
            print(e)
            return False
        self.formcontrol.load_projects()
        self.formcontrol.close_dlg(e=None)
