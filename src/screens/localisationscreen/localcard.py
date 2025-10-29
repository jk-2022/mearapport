# from typing import Any, List, Optional
import os
from flet import *
import sqlite3
# from myaction import recuperer_liste_localisation, recuperer_projet_name
from allpath import AllPath
from screens.localisationscreen.localupdateform import LocalUpdateForm

path=AllPath()
path_data=path.path_data()

from mystorage import *
DB_PATH=os.path.join(path_data,"rapport.db")
ARCHIVES_PATH=path.path_generated_docs()

class LocalCard(Card):
    def __init__(self, page: Page, local, projet, formcontrol):
        super().__init__()
        self.page=page
        self.expand=True
        self.elevation=10
        self.local=local
        self.projet=projet
        self.formcontrol=formcontrol
        
        self.content=Container(
            on_click=lambda e: self.selectlocal(e),
            padding=padding.all(10),
            data=local,
            ink=True,
            expand=True,
            content=Column(
                            [
                                
                        Container(
                            expand=True,
                            content=Column(
                                [
                                    Row(
                                        [
                                            Text(f"Lieu : {local['lieu']} / Localité : {local['localite']} / canton : {local['canton']} / Commune : {local['commune']}", size=11, weight=FontWeight.W_300),
                                        ]
                                    ),
                                    Text(f"Entreprise : {local['entreprise']} / coordonnées : {local['coordonnee_x']};{local['coordonnee_y']}", size=11, weight=FontWeight.W_300),
                                    Row(
                                        [
                                            IconButton(icon=Icons.EDIT, on_click=self.show_edit_local),
                                            IconButton(icon=Icons.DELETE, on_click=self.show_delete_local),
                                        ],
                                        alignment=MainAxisAlignment.END,
                                    )
                                ],spacing=0
                            )
                            ),
                    ],spacing=0
                )
            )
        
    def selectlocal(self,e):
        set_value('local',self.local)
        self.page.go("/recap-ouvrage")
        
    def show_edit_local(self,e):
        cont=LocalUpdateForm(page=self.page, local=self.local, formcontrol=self)
        self.dlg_modal = AlertDialog(
            modal=True,
            title=Text("Modifier projet"),
            content=cont,
            actions=[
                TextButton("Annuler", on_click=self.close_dlg),
                TextButton("Modifier", on_click=cont.SaveData),
            ],
            actions_alignment= MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
            content_padding=0
        )
        self.page.open(self.dlg_modal)
        self.page.update()


    def show_delete_local(self,e):
        self.dlg_modal = AlertDialog(
            modal=True,
            title=Text("Suppression"),
            content=Text(f"Voulez-vous supprimer ?"),
            actions=[
                TextButton("Annuler", on_click=self.close_dlg),
                TextButton("Supprimer", on_click=self.del_local),
            ],
            actions_alignment= MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
            content_padding=0
        )
        self.page.open(self.dlg_modal)
        self.page.update()
        
    def close_dlg(self,e):
        self.page.close(self.dlg_modal)
        self.page.update()
        
    def del_local(self,e):
        pid=int(self.local['id'])
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM localisation WHERE id=?", (pid,))
        conn.commit()
        conn.close()
        self.page.close(self.dlg_modal)
        self.formcontrol.load_localisations()
        
    