
from flet import *

from datetime import datetime
import sqlite3
import os

from allpath import AllPath
from uix.custominputfield import CustomInputField
from uix.custominputnumberfield import CustomInputNumberField

path=AllPath()
path_data=path.path_data()
DB_PATH=os.path.join(path_data,"rapport.db")

# import json
from donnees import *

class SuiviUpdateForm(Container):
    def __init__(self, page: Page, ouvrage_id, donnees, formcontrol):
        super().__init__()
        self.page=page
        width=self.page.window.width-20
        self.width=width
        self.donnees=donnees
        self.ouvrage_id=ouvrage_id
        self.formcontrol=formcontrol

        self.type_reception = Dropdown(label="État de l'ouvrage", options=[
            dropdown.Option("Réception provisoir"),
            dropdown.Option("Réception definitive"),
            dropdown.Option("Suivis"),
        ],expand=True, border_color=Colors.WHITE54 if self.page.theme_mode==ThemeMode.DARK else Colors.BLACK54
        ,value=donnees['type_reception'])

        # dateTime = datetime.now().strftime("%d/%m/%Y")
        self.date_reception = CustomInputField(title="Date de réception", value=donnees['date_reception'])
        self.date_btn=IconButton(icon=Icons.DATE_RANGE, on_click= self.openDatePicker)
        self.participants = CustomInputNumberField(title="Participants.",value=donnees['participants'])
        self.recommandation = CustomInputNumberField(title="Recommandation.", value=donnees['recommandation'])
        self.observation = TextField(label="Observation",height=80, max_lines=4,expand=True, multiline=True,border_color=Colors.WHITE54 if self.page.theme_mode==ThemeMode.DARK else Colors.BLACK54,value=self.donnees['observation'])
    
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
                                self.type_reception
                            ]
                        ),
                        Row(
                            controls=[
                                self.date_reception
                            ]
                        ),
                        Row(
                            controls=[
                                self.participants
                            ]
                        ),
                        Row(
                            controls=[
                                self.recommandation
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
        self.date_reception.value=e.control.value.strftime('%d/%m/%Y')
        self.date_reception.update()

    def handle_dismissal(self,e):
        pass
    
    def update_total_prof(self,e):
        prof_alter=self.date_reception.value or 0
        recommandation=self.recommandation.value or 0
        rest=float(recommandation) + float(prof_alter)
        self.participants.value=rest 
        self.participants.update()

    def openDatePicker(self,e):
        date=DatePicker(
            first_date=datetime(year=2000, month=10, day=1),
            last_date=datetime(year=2025, month=10, day=1),
            on_change=self.handle_change,
            on_dismiss=self.handle_dismissal,
        )
        self.page.open(date)

    def recupererDonnees(self):
        type_reception = self.type_reception.value
        date_reception = self.date_reception.value
        participants = self.participants.value
        recommandation = self.recommandation.value
        observation = self.observation.value
        return {"type_reception": type_reception, "date_reception": date_reception,
                "participants": participants,
                "recommandation": recommandation, "observation":observation
                }

    def SaveData(self, e):
        donnees = self.recupererDonnees()
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        try:
            c = conn.cursor()
            c.execute("""
                        UPDATE  suivi SET  type_reception=?, date_reception=?, participants=?, recommandation=? , observation=? WHERE id=? """, 
                        (donnees["type_reception"], donnees["date_reception"], donnees["participants"], 
                         donnees["recommandation"], donnees['observation'], self.donnees['id'])
                        )
            conn.commit()
        except Exception as e:
            print(e)
            return False
        self.formcontrol.updateData()
        self.formcontrol.close_dlg(e=None)

