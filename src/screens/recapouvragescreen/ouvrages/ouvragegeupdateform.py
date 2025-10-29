
from flet import *

from datetime import datetime
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

class OuvrageUpdateForm(Container):
    def __init__(self, page: Page, local_id, projet_id, donnees, formcontrol):
        super().__init__()
        self.page=page
        width=self.page.window.width-20
        self.width=width
        self.donnees=donnees
        self.local_id=local_id
        self.projet_id=projet_id
        self.formcontrol=formcontrol

        self.type_ouvrage = Dropdown(label="Type d'ouvrage",options=[
        dropdown.Option("PMH"), dropdown.Option("PEA"), dropdown.Option("AEP"), dropdown.Option("PMH en PEA"), dropdown.Option("Mini AEP")
        ],on_change=lambda e :self.update_fields(e)
        ,expand=True,border_color=Colors.WHITE54 if self.page.theme_mode==ThemeMode.DARK else Colors.BLACK38,value=self.donnees['type_ouvrage'])
    
        self.type_reservoir = Dropdown(label="Type réservoir", options=[],
                                       expand=True,
                                       border_color=Colors.WHITE54 if self.page.theme_mode==ThemeMode.DARK else Colors.BLACK38,
                                       value=self.donnees['type_reservoir'])
        for key in reservoirs:
            self.type_reservoir.options.append(dropdown.Option(key))

        self.etat = Dropdown(label="État de l'ouvrage", options=[
            dropdown.Option("Bon état"),
            dropdown.Option("En panne"),
            dropdown.Option("Abandonné")
        ],on_change=lambda e :self.update_field_cause(e)
        ,expand=True, border_color=Colors.WHITE54 if self.page.theme_mode==ThemeMode.DARK else Colors.BLACK38,value=self.donnees['etat'])


        self.numero_irh = CustomInputNumberField(title="Num IRH.", value=donnees['numero_irh'])
        self.annee = CustomInputNumberField(title="Année.", value=donnees['annee'])
        self.type_energie = CustomInputNumberField(title="Prof Total.",value=donnees['type_energie'])
        self.volume_reservoir = CustomInputNumberField(title="Vol reservoir.",value=donnees['volume_reservoir'])
        self.cause = TextField(label="Cause de la panne (si applicable)",border_color=Colors.WHITE54 if self.page.theme_mode==ThemeMode.DARK else Colors.BLACK38,value=self.donnees['cause_panne'])
        self.observation = TextField(label="Observation",height=80, max_lines=4, multiline=True,border_color=Colors.WHITE54 if self.page.theme_mode==ThemeMode.DARK else Colors.BLACK38,value=self.donnees['observation'],expand=True)
    
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
                                self.type_ouvrage
                            ]
                        ),
                        Row(
                            controls=[
                                self.annee, self.numero_irh
                            ]
                        ),
                        Row(
                            controls=[
                                self.volume_reservoir,
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
            self.volume_reservoir.visible=False
            self.numero_irh.visible=True
        else:
            self.type_energie.visible=True
            self.type_reservoir.visible=True
            self.volume_reservoir.visible=True
            self.numero_irh.visible=False
        self.page.update()

    def update_field_cause(self,e):
        ouvrage=e.control.value
        if ouvrage=="En panne" or ouvrage=="Abandonné":
            self.cause.visible=True
        else:
            self.cause.visible=False
        self.page.update()

    def handle_change(self,e):
        self.type_ouvrage.value=e.control.value.strftime('%d/%m/%Y')
        self.type_ouvrage.update()

    def handle_dismissal(self,e):
        ""
    
    def update_total_prof(self,e):
        prof_alter=self.numero_irh.value or 0
        annee=self.annee.value or 0
        rest=float(annee) + float(prof_alter)
        self.type_energie.value=rest 
        self.type_energie.update()

    def openDatePicker(self,e):
        date=DatePicker(
            first_date=datetime(year=2000, month=10, day=1),
            last_date=datetime(year=2025, month=10, day=1),
            on_change=self.handle_change,
            on_dismiss=self.handle_dismissal,
        )
        self.page.open(date)

    def recupererDonnees(self):
        type_ouvrage = self.type_ouvrage.value
        numero_irh = self.numero_irh.value
        annee = self.annee.value
        type_energie = self.type_energie.value
        volume_reservoir = self.volume_reservoir.value
        etat = self.etat.value
        cause = self.cause.value
        observation = self.observation.value
        return {"type_ouvrage": type_ouvrage, "numero_irh": numero_irh,
                "annee": annee,"type_energie": type_energie, "volume_reservoir": volume_reservoir,
                "etat": etat, "cause_panne": cause,
                "observation":observation
                }

    def SaveData(self, e):
        donnees = self.recupererDonnees()
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)

        try:
            c = conn.cursor()
            c.execute("""
                        UPDATE  ouvrages SET  type_ouvrage=?, numero_irh=?, annee=?, type_energie=?, volume_reservoir=?, etat=?, cause_panne=?, observation=? WHERE projet_id=? AND localisation_id=?""", (donnees["type_ouvrage"], donnees["numero_irh"], donnees["annee"],
                        donnees["type_energie"], donnees["volume_reservoir"], donnees["etat"], donnees["cause_panne"], donnees['observation'], self.projet_id, self.donnees['localisation_id'])
                        )
            conn.commit()
        except Exception as e:
            print(e)
            return False
        self.formcontrol.updateData()
        self.formcontrol.close_dlg(e=None)

