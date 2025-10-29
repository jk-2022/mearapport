from typing import Any, List, Optional
from flet import *

import sqlite3
import os

from allpath import AllPath
from myaction import load_all_entreprise
path=AllPath()
path_data=path.path_data()
DB_PATH=os.path.join(path_data,"rapport.db")

from donnees import *

from uix.custominputfield import CustomInputField

class LocalUpdateForm(Container):
    def __init__(self, page: Page, local, formcontrol):
        super().__init__()
        self.padding = 0
        self.page=page
        self.local=local
        self.formcontrol=formcontrol

        self.date = Text(f"{local['created_at']}")

        self.prefecture = Dropdown(label="Préfecture", options=[
        ],expand=True,border_color=Colors.WHITE54 if self.page.theme_mode==ThemeMode.DARK else Colors.BLACK38,
        on_change=lambda e :self.update_commune(e),
        value=self.local['prefecture'])
        for key in donnees.keys():
            self.prefecture.options.append(dropdown.Option(key))

        self.commune = Dropdown(label="Commune", options=[
                ],expand=True,border_color=Colors.WHITE54 if self.page.theme_mode==ThemeMode.DARK else Colors.BLACK38,
                 value=local['commune'])
        
        for value in donnees[self.local['prefecture']]:
                self.commune.options.append(dropdown.Option(value))

        
        self.choix_entreprise = Dropdown(label="Entreprise", options=[
        ],expand=True,border_color=Colors.WHITE54 if self.page.theme_mode==ThemeMode.DARK else Colors.BLACK38,
        on_change=lambda e :self.update_commune(e),value=local['entreprise'])
        
        liste_entreprise=load_all_entreprise()
        if liste_entreprise:
            for dict_data in liste_entreprise:
                self.choix_entreprise.options.append(dropdown.Option(dict_data['nom']))
       
        self.add_bnt_entr=IconButton(icon=Icons.ADD, on_click=self.showNameEntrepriseField)
        self.canton = CustomInputField(title="Canton",value=local['canton'])
        self.localite = CustomInputField(title="Localité",value=local['localite'])
        self.lieu = CustomInputField(title="Lieu d'implantation",value=local['lieu'])
        self.coordonnee_x = CustomInputField(title="Coordonnee X",value=local['coordonnee_x'])
        self.coordonnee_y = CustomInputField(title="Coordonnee Y",value=local['coordonnee_y'])
        self.nom_entreprise = CustomInputField(title="Nom entreprise")
        self.save_btn=IconButton(icon=Icons.SAVE, on_click=self.saveContact)

        self. choix_entreprise_cnt=Row(
                            controls=[
                                self.choix_entreprise,self.add_bnt_entr
                            ]
                        )

        self.entre_cnt=Container(
            border=border.all(1, Colors.YELLOW_400),
            padding=5,
            border_radius=5,
            content=Row(
                        [
                            self.nom_entreprise,self.save_btn
                        ]
                    )
        )
        self.entre_cnt.visible=False

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
                                self.prefecture,self.commune
                            ]
                        ),
                        Row(
                            controls=[
                                self.canton,self.localite
                            ]
                        ),
                        self.lieu,
                        Row(
                            controls=[
                                self.coordonnee_x,self.coordonnee_y
                            ]
                        ),
                        self.choix_entreprise_cnt,
                        self.entre_cnt
                    ]
                )
            )
        )

    def update_commune(self,e):
        self.commune.options.clear()
        for key in donnees.keys():
            if self.prefecture.value==key:
                for value in donnees[key]:
                    self.commune.options.append(dropdown.Option(value))
        self.commune.update()
    
    def updateEntrepriseChoice(self,e):
        self.choix_entreprise.options.clear()
        liste_entreprise=load_all_entreprise()
        if liste_entreprise:
            for dict_data in liste_entreprise:
                self.choix_entreprise.options.append(dropdown.Option(dict_data['nom']))
        self.choix_entreprise.update()

    def showNameEntrepriseField(self,e):
        self.entre_cnt.visible=True
        self.choix_entreprise_cnt.visible=False
        self.entre_cnt.update()
        self.choix_entreprise_cnt.update()
    
    def saveContact(self,e):
        nom_entreprise = self.nom_entreprise.value
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        try:
            c = conn.cursor()
            c.execute("""
                        INSERT INTO entreprise('nom','contact') VALUES(?,?)
                        """, (nom_entreprise,""))
            conn.commit()
        except Exception as e:
            print(e)
            return False
        self.updateEntrepriseChoice(e=None)
        self.entre_cnt.visible=False
        self.choix_entreprise_cnt.visible=True
        self.choix_entreprise_cnt.update()
        self.entre_cnt.update()

    def recupererDonnees(self):
        prefecture = self.prefecture.value
        commune = self.commune.value
        canton = self.canton.value
        localite = self.localite.value
        lieu = self.lieu.value
        coordonnee_x = self.coordonnee_x.value
        coordonnee_y = self.coordonnee_y.value
        entreprise = self.choix_entreprise.value
        return {"prefecture": prefecture, "commune": commune, "canton": canton,
                "localite": localite,"lieu": lieu, "coordonnee_x": coordonnee_x, 
                "coordonnee_y": coordonnee_y,"entreprise": entreprise}
        
    def SaveData(self, e):
        donnees = self.recupererDonnees()
        pid=self.local['id']
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        try:
            c = conn.cursor()
            c.execute("UPDATE localisation SET prefecture=?, commune=?, canton=?, localite=?, lieu=?, coordonnee_x=?, coordonnee_y=?, entreprise=? WHERE id=?", (donnees["prefecture"], donnees["commune"], donnees["canton"],
                donnees["localite"], donnees["lieu"], donnees["coordonnee_x"], donnees["coordonnee_y"], donnees["entreprise"], pid))
            conn.commit()
        except Exception as e:
            print(e)
            return False
        self.formcontrol.close_dlg(e=None)
        self.formcontrol.formcontrol.load_localisations()
