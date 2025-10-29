
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

class ForationForm(Container):
    def __init__(self, page: Page, local_id, formcontrol):
        super().__init__()
        self.page=page
        width=self.page.window.width-20
        self.width=width
        self.local_id=local_id
        self.formcontrol=formcontrol

        dateTime = datetime.now().strftime("%d/%m/%Y")
        self.date_foration = CustomInputField(title="Date Foration",value=dateTime)
        self.date_btn=IconButton(icon=Icons.DATE_RANGE, on_click= self.openDatePicker)
        self.prof_alteration = CustomInputNumberField(title="Prof Alteration",on_change=self.update_total_prof)
        self.prof_socle = CustomInputNumberField(title="Prof Socle",on_change=self.update_total_prof)
        self.prof_total = CustomInputNumberField(title="Prof Total", read_only=True)
        self.debit_soufflage = CustomInputNumberField(title="Débit soufflage")
        self.prof_tube_plein = CustomInputNumberField(title="Prof. Tube plein")
        self.prof_tube_crepine = CustomInputNumberField(title="Prof. Tube crepine")
        self.observation = TextField(label="Observation", max_lines=4, multiline=True,border_color=Colors.WHITE54 if self.page.theme_mode==ThemeMode.DARK else Colors.BLACK38,expand=True)
    

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
                                self.date_foration,self.date_btn
                            ]
                        ),
                        Row(
                            controls=[
                                self.prof_alteration, self.prof_socle
                            ]
                        ),
                        Row(
                            controls=[
                                self.debit_soufflage, self.prof_total
                            ]
                        ),
                        Row(
                            controls=[
                                self.prof_tube_plein,self.prof_tube_crepine
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
    def handle_change(self,e):
        self.date_foration.value=e.control.value.strftime('%d/%m/%Y')
        self.date_foration.update()

    def handle_dismissal(self,e):
        ""
    
    def update_total_prof(self,e):
        prof_alter=self.prof_alteration.value or 0
        prof_socle=self.prof_socle.value or 0
        rest=float(prof_socle) + float(prof_alter)
        self.prof_total.value=rest 
        self.prof_total.update()

    def openDatePicker(self,e):
        date=DatePicker(
            first_date=datetime(year=2000, month=10, day=1),
            last_date=datetime(year=2025, month=10, day=1),
            on_change=self.handle_change,
            on_dismiss=self.handle_dismissal,
        )
        self.page.open(date)

    def recupererDonnees(self):
        date_foration = self.date_foration.value
        prof_alteration = self.prof_alteration.value
        prof_socle = self.prof_socle.value
        prof_total = self.prof_total.value
        debit_soufflage = self.debit_soufflage.value
        prof_tube_plein = self.prof_tube_plein.value
        prof_tube_crepine = self.prof_tube_crepine.value
        observation = self.observation.value
        return {"date_foration": date_foration, "prof_alteration": prof_alteration,
                "prof_socle": prof_socle,"prof_total": prof_total, "debit_soufflage": debit_soufflage
                , "prof_tube_plein": prof_tube_plein
                , "prof_tube_crepine": prof_tube_crepine
                , "observation": observation
                }

    def SaveData(self, e):
        donnees = self.recupererDonnees()
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)

        try:
            c = conn.cursor()
            c.execute("""
                        INSERT INTO foration('localisation_id', 'date_foration', 'prof_alteration', 'prof_socle', 'prof_total', 'debit_soufflage', 'prof_tube_plein', 'prof_tube_crepine', 'observation') VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (self.local_id, donnees["date_foration"], donnees["prof_alteration"], donnees["prof_socle"],
                        donnees["prof_total"], donnees["debit_soufflage"], donnees["prof_tube_plein"], donnees["prof_tube_crepine"], donnees["observation"])
                        )
            conn.commit()
        except Exception as e:
            print(e)
            return False
        self.formcontrol.updateData()
        self.formcontrol.close_dlg(e=None)

