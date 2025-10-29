
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

class PanneUpdateForm(Container):
    def __init__(self, page: Page, ouvrage_id, donnees, formcontrol):
        super().__init__()
        self.page=page
        width=self.page.window.width-20
        self.width=width
        self.donnees=donnees
        self.ouvrage_id=ouvrage_id
        self.formcontrol=formcontrol

        # dateTime = datetime.now().strftime("%d/%m/%Y")
        self.date_signaler = CustomInputField(title="Date signaler", value=donnees['date_signaler'])
        self.date_btn=IconButton(icon=Icons.DATE_RANGE, on_click= self.openDatePicker)
        self.description = TextField(label="Descriptions",height=80, max_lines=4,expand=True, multiline=True,border_color=Colors.WHITE54 if self.page.theme_mode==ThemeMode.DARK else Colors.BLACK38,value=self.donnees['description'])
        self.solution = TextField(label="Solutions",height=80, max_lines=4,expand=True, multiline=True,border_color=Colors.WHITE54 if self.page.theme_mode==ThemeMode.DARK else Colors.BLACK38,value=self.donnees['solution'])
        self.observation = TextField(label="Observation",height=80, max_lines=4,expand=True, multiline=True,border_color=Colors.WHITE54 if self.page.theme_mode==ThemeMode.DARK else Colors.BLACK38,value=self.donnees['observation'])
    
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
        pass
    
    def update_total_prof(self,e):
        prof_alter=self.date_signaler.value or 0
        solution=self.solution.value or 0
        rest=float(solution) + float(prof_alter)
        self.description.value=rest 
        self.description.update()

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
                "description": description,
                "solution": solution, "observation":observation
                }

    def SaveData(self, e):
        donnees = self.recupererDonnees()
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        try:
            c = conn.cursor()
            c.execute("""
                        UPDATE  pannes SET  date_signaler=?, description=?, solution=? , observation=? WHERE id=? """, 
                        (donnees["date_signaler"], donnees["description"], 
                         donnees["solution"], donnees['observation'], self.donnees['id'])
                        )
            conn.commit()
        except Exception as e:
            print(e)
            return False
        self.formcontrol.updateData()
        self.formcontrol.close_dlg(e=None)

