from flet import *

# from datetime import datetime
import sqlite3
import os

from allpath import AllPath
from uix.custominputnumberfield import CustomInputNumberField
path=AllPath()
path_data=path.path_data()
DB_PATH=os.path.join(path_data,"rapport.db")

# import json
from donnees import *
from uix.custominputfield import CustomInputField

class OuvrageForm(Container):
    def __init__(self, page: Page, local_id, projet_id, formcontrol):
        super().__init__()
        self.page=page
        width=self.page.window.width-20
        self.width=width
        self.local_id=local_id
        self.projet_id=projet_id
        self.formcontrol=formcontrol

        self.type_ouvrage = Dropdown(label="Type d'ouvrage", options=[
        dropdown.Option("PMH"), dropdown.Option("PEA"), dropdown.Option("PMH en PEA"), dropdown.Option("AEP"), dropdown.Option("Mini AEP")
        ]
        ,on_change=lambda e :self.update_fields(e)
        ,expand=True,border_color=Colors.WHITE54 if self.page.theme_mode==ThemeMode.DARK else Colors.BLACK38)
        # self.type_ouvrage.visible=False

        self.type_reservoir = Dropdown(label="Type réservoir", options=[
        ],expand=True,border_color=Colors.WHITE54 if self.page.theme_mode==ThemeMode.DARK else Colors.BLACK38)
        for key in reservoirs:
            self.type_reservoir.options.append(dropdown.Option(key))

        self.etat = Dropdown(label="État de l'ouvrage", options=[
            dropdown.Option("Bon état"),
            dropdown.Option("En panne"),
            dropdown.Option("Abandonné")
        ],on_change = lambda e :self.update_field_cause(e)
        ,expand=True, border_color=Colors.WHITE54 if self.page.theme_mode==ThemeMode.DARK else Colors.BLACK38)

        self.numero_irh = CustomInputNumberField(title="N° IRH")
        self.numero_irh.visible=False
        self.type_reservoir.visible=False
        self.type_energie = CustomInputField(title="Type énergie")
        self.type_energie.visible=False
        self.annee = CustomInputNumberField(title="Année d'impl.")
        self.volume = CustomInputNumberField(title="Vol. réservoir")
        self.volume.visible = False
        self.cause = TextField(label="Cause de la panne (si applicable)",border_color=Colors.WHITE54 if self.page.theme_mode==ThemeMode.DARK else Colors.BLACK38)
        self.cause.visible=False
        self.observation = TextField(label="Observation",height=80, max_lines=4, multiline=True,border_color=Colors.WHITE54 if self.page.theme_mode==ThemeMode.DARK else Colors.BLACK38,expand=True)

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
                                self.type_ouvrage, self.numero_irh
                            ]
                        ),
                        Row(
                            controls=[
                                self.type_reservoir
                            ]
                        ),
                        Row(
                            controls=[
                                self.type_energie
                            ]
                        ),
                        Row(
                            controls=[
                                self.volume, self.annee
                            ]
                        ),
                        Row(
                            controls=[
                                self.etat
                            ]
                        ),
                        Row(
                            controls=[
                                self.cause
                            ]
                        ),
                        Row(
                            controls=[
                                self.observation
                            ]
                        ),
                    ]
                )
            )
        )

    def update_fields(self,e):
        ouvrage=e.control.value
        if ouvrage=="PMH" or ouvrage=="PMH en PEA":
            self.type_energie.visible=False
            self.type_reservoir.visible=False
            self.volume.visible=False
            self.numero_irh.visible=True
        else:
            self.type_energie.visible=True
            self.type_reservoir.visible=True
            self.volume.visible=True
            self.numero_irh.visible=False
        self.page.update()

    def update_field_cause(self,e):
        ouvrage=e.control.value
        if ouvrage=="En panne" or ouvrage=="Abandonné":
            self.cause.visible=True
        else:
            self.cause.visible=False
        self.page.update()

    def recupererDonnees(self):
        type_ouvrage = self.type_ouvrage.value
        numero_irh = self.numero_irh.value
        type_reservoir = self.type_reservoir.value
        type_energie = self.type_energie.value
        annee = self.annee.value
        volume = self.volume.value
        etat = self.etat.value
        cause_panne=self.cause.value
        observation = self.observation.value
        return {"type_ouvrage": type_ouvrage,"numero_irh": numero_irh, "type_reservoir": type_reservoir,
                "type_energie": type_energie,"annee": annee, 
                "volume_reservoir": volume, "etat": etat, "cause_panne":cause_panne,
                "observation": observation
                }

    def SaveData(self, e):
        donnees = self.recupererDonnees()
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        try:
            c = conn.cursor()
            c.execute("""
                        INSERT INTO ouvrages('projet_id','localisation_id', 'type_ouvrage', 'numero_irh', 'type_reservoir', 'type_energie', 'annee', 'volume_reservoir', 'etat', 'cause_panne','observation') VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (self.projet_id, self.local_id, donnees["type_ouvrage"], donnees["numero_irh"], donnees["type_reservoir"], donnees["type_energie"],
                        donnees["annee"], donnees["volume_reservoir"], donnees["etat"], donnees["cause_panne"], donnees["observation"])
                        )
            conn.commit()
            # ouvrage_id = c.lastrowid
            # self.page.client_storage.set('ouvrage_id',ouvrage_id)
        except Exception as e:
            print(e)
            return False
        self.formcontrol.updateData()
        self.formcontrol.formcontrol.updateBtn()
        self.formcontrol.close_dlg(e=None)
