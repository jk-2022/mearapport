
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

class SuiviForm(Container):
    def __init__(self, page: Page, ouvrage_id, formcontrol):
        super().__init__()
        self.page=page
        width=self.page.window.width-20
        self.width=width
        self.ouvrage_id=ouvrage_id
        self.formcontrol=formcontrol

        self.type_reception = Dropdown(label="État de l'ouvrage", options=[
            dropdown.Option("Réception provisoir"),
            dropdown.Option("Réception definitive"),
            dropdown.Option("Suivis"),
        ],expand=True,border_color=Colors.WHITE54 if self.page.theme_mode==ThemeMode.DARK else Colors.BLACK38)

        dateTime = datetime.now().strftime("%d/%m/%Y")
        self.date_reception = CustomInputField(title="Date reception.", value=dateTime)
        self.date_btn=IconButton(icon=Icons.DATE_RANGE, on_click= self.openDatePicker)
        # self.type_reception = CustomInputNumberField(title="Type reception")
        self.recommandation = TextField(label="Recommandations",height=80, max_lines=4, multiline=True,border_color=Colors.WHITE54 if self.page.theme_mode==ThemeMode.DARK else Colors.BLACK38,expand=True)
        self.participants = TextField(label="Participants",height=80, max_lines=4, multiline=True,border_color=Colors.WHITE54 if self.page.theme_mode==ThemeMode.DARK else Colors.BLACK38,expand=True)
        self.observation = TextField(label="Observations",height=80, max_lines=4, multiline=True,border_color=Colors.WHITE54 if self.page.theme_mode==ThemeMode.DARK else Colors.BLACK38,expand=True)
    
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
        ""

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
                "participants": participants,"recommandation": recommandation, 
                "observation": observation
                }

    def SaveData(self, e):
        donnees = self.recupererDonnees()
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        try:
            c = conn.cursor()
            c.execute("""
                        INSERT INTO suivi('ouvrage_id', 'type_reception', 'date_reception', 'participants', 'recommandation', 'observation') VALUES(?, ?, ?, ?, ?, ?)
                        """, (self.ouvrage_id, donnees["type_reception"], donnees["date_reception"], 
                              donnees["participants"],donnees["recommandation"], donnees["observation"])
                        )
            conn.commit()
        except Exception as e:
            print(e)
            return False
        # status=self.page.client_storage.get('save_from')
        # if status=='click_btn':
        #     self.formcontrol.updateData()
        # else:
        self.formcontrol.updateData()
        self.formcontrol.close_dlg(e=None)

