import os
import sqlite3
from flet import *

from myaction import load_one_panne
from .panneform import PanneForm
from .panneupdateform import PanneUpdateForm
from uix.customtitlelabel import CustomTitleLabel

from allpath import AllPath
path=AllPath()
path_data=path.path_data()

DB_PATH=os.path.join(path_data,"rapport.db")
ARCHIVES_PATH=path.path_generated_docs()

class PanneControl(Card):
    def __init__(self, page: Page, donnees):
        super().__init__()
        self.page=page
        self.donnees=donnees
        self.ouvrage_id=donnees['id']
        print('self.ouvrage_id',self.ouvrage_id)
        self.elevation=5
        self.cont=Column( spacing=0)
        self.label= Text(f"Pannes",text_align=TextAlign.CENTER,color=Colors.GREY_500)
        self.delete_btn=ElevatedButton('Supprimer',icon=Icons.DELETE,icon_color=Colors.RED,on_click=self.showDelete)
        self.delete_btn.visible=False

        self.content=Container(
            border_radius=10,
            border=border.all(1,Colors.GREY_500),
            expand=True,
            content=Column(
                [
                    Row(
                        [
                           self.label
                        ],alignment=MainAxisAlignment.CENTER
                    ),
                    self.cont,
                    Row(
                        [
                            ElevatedButton('Modifier',icon=Icons.UPDATE,icon_color=Colors.GREEN_500,on_click=self.showUpdateData),
                            self.delete_btn,
                        ],alignment=MainAxisAlignment.SPACE_EVENLY
                    )
                ]
            )
        )

        self.updateData()
    
    def updateData(self):
        donnees=load_one_panne(self.donnees['id'])
        self.donnees=donnees
        self.cont.controls.clear()
        if donnees:
            self.delete_btn.visible=True
            list_item=['id','ouvrage_id', 'created_at']
            for key, val in donnees.items():
                if key in list_item or val=="" or val==None:
                    pass 
                else:
                    # self.label.value=f"{donnees['type_reception']}"
                    self.cont.controls.append(
                        CustomTitleLabel(title=key,value=val)
                    )
        else:
            self.delete_btn.visible=False
            self.cont.controls.append(Row(
                [
                    Text("Pas de données pannes enrégistré")
                ],alignment=MainAxisAlignment.CENTER))
        try:
            # self.label.update()
            self.delete_btn.update()
            self.cont.update()
        except:
            pass

    def showDelete(self,e):
        self.dlg_modal = AlertDialog(
            modal=True,
            title=Text("Confirmation"),
            content=Row(
                [
                    Text(f"Voulez-vous supprimer ?")
                ],alignment=MainAxisAlignment.CENTER
            ),
            actions=[
                TextButton("Non", on_click=self.close_dlg),
                TextButton("Oui", on_click=self.del_ouvrage, icon=Icons.DELETE, icon_color=Colors.RED),
            ],
            actions_alignment= MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
            content_padding=0
        )
        self.page.open(self.dlg_modal)
        self.page.update()
        
    def del_ouvrage(self,e):
        rid=int(self.donnees['id'])
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM pannes WHERE id=?", (rid,))
        conn.commit()
        conn.close()
        self.page.close(self.dlg_modal)
        self.updateData()

    
    def showUpdateData(self,e):
        if self.donnees==[]:
            cont=PanneForm(page=self.page,ouvrage_id=self.ouvrage_id, formcontrol=self)
        else:
            cont=PanneUpdateForm(page=self.page,ouvrage_id=self.ouvrage_id, donnees=self.donnees, formcontrol=self)
        self.dlg_modal = AlertDialog(
            modal=True,
            title=Text("Nouvel Evènement"),
            content=cont,
            actions=[
                TextButton("Annuler", on_click=self.close_dlg),
                TextButton("Sauvegarder", on_click=cont.SaveData),
            ],
            actions_alignment= MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
            content_padding=0
        )
        self.page.open(self.dlg_modal)
        self.page.update()

    def close_dlg(self, e):
        self.page.close(self.dlg_modal)
        self.page.update()

