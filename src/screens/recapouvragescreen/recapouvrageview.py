import os
# import sqlite3
from flet import *

from myaction import load_all_data, load_all_panne, load_all_reception
from .pannes.pannecontrol import PanneControl
from .pannes.panneform import PanneForm
from .suivi.suivicontrol import SuiviControl
from .localrecapcard import LocalRecapCard
from .ouvrages.ouvragecontrol import OuvrageControl
from .suivi.suiviform import SuiviForm
from .pompage.pompagecontrol import PompageControl
from .foration.forationcontrol import ForationControl
from allpath import AllPath

path=AllPath()
path_data=path.path_data()

from mystorage import *

DB_PATH=os.path.join(path_data,"rapport.db")
ARCHIVES_PATH=path.path_generated_docs()

class RecapOuvrageView(View):
    def __init__(self, page : Page,route:str="/recap-ouvrage"):
        super().__init__()
        self.page=page
        self.projet=get_value('projet')
        self.local=get_value('local')
        
        self.receptions_cnt=Column(expand=True)
        self.pannes_cnt=Column(expand=True)

        self.btn_add_panne=ElevatedButton('Add un panne',icon=Icons.ADD, on_click=self.showNewPanne)
        self.btn_add_panne.visible=False
        self.btn_add_event=ElevatedButton('Add un évènement',icon=Icons.ADD, on_click=self.showNewSuivi)
        self.btn_add_event.visible=False

        self.all_data=load_all_data(self.local['id'])
        # print(self.all_data)

        if self.all_data['ouvrages']:
            self.ouvrage_id=self.all_data['ouvrages'][0]['id']
            self.updateData()

        self.ouvrages_cnt=OuvrageControl(page=self.page, donnees=self.all_data['ouvrages'], local_id=self.local['id'],projet_id=self.projet['id'], formcontrol=self)
        self.pompage_cnt=PompageControl(page=self.page, donnees=self.all_data['pompage'], local_id=self.local['id'])
        self.foration_cnt=ForationControl(page=self.page, donnees=self.all_data['foration'], local_id=self.local['id'])

        self.controls.append(
            SafeArea(
                Column(
                    controls=[
                        Row(
                            [IconButton(icon=Icons.ARROW_BACK,on_click=self.page.on_view_pop),]
                        ),
                        Row(
                            [
                                self.btn_add_panne,
                                self.btn_add_event,
                             ],alignment=MainAxisAlignment.END
                        ),
                        Column(
                            [
                            LocalRecapCard(page=self.page, donnees=self.local),
                            self.ouvrages_cnt,
                            self.pannes_cnt,
                            self.receptions_cnt,
                            self.pompage_cnt,
                            self.foration_cnt,
                            ],expand=True, scroll=ScrollMode.ALWAYS
                        )
                    ],expand=True
                    ,spacing=5
                ),expand=True
            )
        )

    def get_ouvrage_id(self):
        all_data=load_all_data(self.local['id'])
        # print(all_data)
        if all_data['ouvrages']:
            ouvrage_id=all_data['ouvrages'][0]['id']
            return ouvrage_id
        else:
            return None
    
    def updateBtn(self):
        self.btn_add_panne.visible=True
        self.btn_add_event.visible=True
        self.btn_add_panne.update()
        self.btn_add_event.update()
    
    def updateData(self):
        self.ouvrage_id=self.all_data['ouvrages'][0]['id']
        set_value('ouvrage_id', self.ouvrage_id)
        receptions=load_all_reception(self.ouvrage_id)
        if receptions:
            self.receptions_cnt.controls.clear()
            for reception in receptions:
                self.receptions_cnt.controls.append(
                    SuiviControl(page=self.page, donnees=reception)
                )

        pannes=load_all_panne(self.ouvrage_id)
        if pannes:
            self.pannes_cnt.controls.clear()
            for reception in pannes:
                self.pannes_cnt.controls.append(
                    PanneControl(page=self.page, donnees=reception)
                )
        self.btn_add_panne.visible=True
        self.btn_add_event.visible=True

    def showNewSuivi(self,e):
        ouvrage_id=self.get_ouvrage_id()
        cont=SuiviForm(page=self.page, ouvrage_id=ouvrage_id, formcontrol=self)
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
    
    def showNewPanne(self,e):
        ouvrage_id=self.get_ouvrage_id()
        cont=PanneForm(page=self.page, ouvrage_id=ouvrage_id, formcontrol=self)
        self.dlg_modal = AlertDialog(
            modal=True,
            title=Text("Nouvel Panne"),
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

    def close_dlg(self,e):
        self.page.close(self.dlg_modal)
        self.page.update()