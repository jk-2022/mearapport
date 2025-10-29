
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

class PanneForm(Container):
    def __init__(self, page: Page, ouvrage_id, formcontrol):
        super().__init__()
        self.page=page
        width=self.page.window.width-20
        self.width=width
        self.ouvrage_id=ouvrage_id
        self.formcontrol=formcontrol

        dateTime = datetime.now().strftime("%d/%m/%Y")
        self.date_btn=IconButton(icon=Icons.DATE_RANGE, on_click= self.openDatePicker)
        self.date_signaler = CustomInputField(title="Date reception.", value=dateTime)
        self.description = TextField(label="Description",height=80, max_lines=4, multiline=True,border_color=Colors.WHITE54 if self.page.theme_mode==ThemeMode.DARK else Colors.BLACK38,expand=True)
        # self.type_reception = CustomInputNumberField(title="Type reception")
        self.solution = TextField(label="Solutions",height=80, max_lines=4, multiline=True,border_color=Colors.WHITE54 if self.page.theme_mode==ThemeMode.DARK else Colors.BLACK38,expand=True)
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
                                self.date_signaler,self.date_btn
                            ]
                        ),
                        Row(
                            controls=[
                                self.description
                            ]
                        ),
                        Row(
                            controls=[
                                self.solution
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
        self.date_signaler.value=e.control.value.strftime('%d/%m/%Y')
        self.date_signaler.update()

    def handle_dismissal(self,e):
        ""

    def openDatePicker(self,e):
        date=DatePicker(
            first_date=datetime(year=2000, month=10, day=1),
            last_date=datetime(year=2026, month=10, day=1),
            on_change=self.handle_change,
            on_dismiss=self.handle_dismissal,
        )
        self.page.open(date)

    def recupererDonnees(self):
        date_signaler = self.date_signaler.value
        description = self.description.value
        solution = self.solution.value
        observation = self.observation.value
        return {"date_signaler": date_signaler,
                "description": description,"solution": solution, 
                "observation": observation
                }

    def SaveData(self, e):
        donnees = self.recupererDonnees()
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        try:
            c = conn.cursor()
            c.execute("""
                        INSERT INTO pannes('ouvrage_id', 'date_signaler', 'description', 'solution', 'observation') VALUES( ?, ?, ?, ?, ?)
                        """, (self.ouvrage_id, donnees["date_signaler"], 
                              donnees["description"],donnees["solution"], donnees["observation"])
                        )
            conn.commit()
        except Exception as e:
            print(e)
            return False
        self.formcontrol.updateData()
        self.formcontrol.close_dlg(e=None)

