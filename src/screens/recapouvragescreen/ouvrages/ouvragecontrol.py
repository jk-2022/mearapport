import os
import sqlite3
from flet import *

from myaction import load_all_data
from .ouvrageform import OuvrageForm
from .ouvragegeupdateform import OuvrageUpdateForm
from uix.customtitlelabel import CustomTitleLabel

from allpath import AllPath
path=AllPath()
path_data=path.path_data()

from mystorage import *
DB_PATH=os.path.join(path_data,"rapport.db")
ARCHIVES_PATH=path.path_generated_docs()

class OuvrageControl(Card):
    def __init__(self, page: Page, donnees, local_id, projet_id,formcontrol):
        super().__init__()
        self.page=page
        self.donnees=donnees
        self.local_id=local_id
        self.projet_id=projet_id
        self.formcontrol=formcontrol
        self.elevation=5
        self.cont=Column( spacing=0)

        self.delete_btn=ElevatedButton('Supprimer',icon=Icons.DELETE,icon_color=Colors.RED,on_click=self.showDelete)
        self.delete_btn.visible=False

        self.content=Container(
            border_radius=10,
            border=border.all(1,Colors.GREEN_500),
            expand=True,
            content=Column(
                [
                    Row(
                        [
                            Text("Ouvrage",text_align=TextAlign.CENTER,color=Colors.GREEN_500)
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
        rid=int(self.donnees[0]['id'])
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ouvrages WHERE id=?", (rid,))
        conn.commit()
        conn.close()
        self.page.close(self.dlg_modal)
        self.updateData()

    def updateData(self):
        self.local=get_value('local')
        all_data=load_all_data(self.local['id'])
        donnees=all_data['ouvrages']
        self.donnees=donnees
        self.cont.controls.clear()
        if donnees:
            self.delete_btn.visible=True
            list_item=['id','projet_id','localisation_id','created_at']
            for key, val in donnees[0].items():
                if key in list_item or val=="" or val==None:
                    pass 
                else:
                    self.cont.controls.append(
                        CustomTitleLabel(title=key,value=val)
                    )
        else:
            self.delete_btn.visible=False
            self.cont.controls.append(Row(
                [
                    Text("Pas de données D'OUVRAGE enrégistré")
                ],alignment=MainAxisAlignment.CENTER))
        try:
            self.delete_btn.update()
            self.cont.update()
        except:
            pass

    
    def showUpdateData(self,e):
        if self.donnees==[]:
            cont=OuvrageForm(page=self.page,local_id=self.local_id, projet_id=self.projet_id, formcontrol=self)
        else:
            cont=OuvrageUpdateForm(page=self.page,local_id=self.local_id, projet_id=self.projet_id, donnees=self.donnees[0], formcontrol=self)
        self.dlg_modal = AlertDialog(
            modal=True,
            title=Text("Info Ouvrage"),
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

