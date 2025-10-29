
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

class PompageUpdateForm(Container):
    def __init__(self, page: Page, local_id, donnees, formcontrol):
        super().__init__()
        self.page=page
        width=self.page.window.width-20
        self.width=width
        self.donnees=donnees
        self.local_id=local_id
        self.formcontrol=formcontrol

        # print(donnees)
        # dateTime = datetime.now().strftime("%d/%m/%Y")
        self.date_pompage = CustomInputField(title="Date Foration.",value=donnees['date_pompage'])
        self.date_btn=IconButton(icon=Icons.DATE_RANGE, on_click= self.openDatePicker)
        self.type_pompe = CustomInputField(title="Prof Alteration.",on_change=self.update_total_prof,value=donnees['type_pompe'])
        self.cote_pompe = CustomInputNumberField(title="Prof Socle.",on_change=self.update_total_prof,value=donnees['cote_pompe'])
        self.temps_pompage = CustomInputNumberField(title="Prof Total.",value=donnees['temps_pompage'])
        self.debit_pompage = CustomInputNumberField(title="Débit soufflage.",value=donnees['debit_pompage'])
        self.niv_dynamique = CustomInputNumberField(title="Prof. Tube plein.",value=donnees['niv_dynamique'])
        self.niv_statique = CustomInputNumberField(title="Prof. Tube crepine.",value=donnees['niv_statique'])
        self.observation = TextField(label="Observation",height=80, max_lines=4, multiline=True,border_color=Colors.WHITE54 if self.page.theme_mode==ThemeMode.DARK else Colors.BLACK38,expand=True,value=self.donnees['observation'])
    
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
                                self.date_pompage,self.date_btn
                            ]
                        ),
                        Row(
                            controls=[
                                self.type_pompe, self.cote_pompe
                            ]
                        ),
                        Row(
                            controls=[
                                self.temps_pompage, self.debit_pompage
                            ]
                        ),
                        Row(
                            controls=[
                                self.niv_dynamique, self.niv_statique
                            ]
                        ),
                    ]
                )
            )
        )

    def handle_change(self,e):
        self.date_pompage.value=e.control.value.strftime('%d/%m/%Y')
        self.date_pompage.update()

    def handle_dismissal(self,e):
        ""
    
    def update_total_prof(self,e):
        prof_alter=self.type_pompe.value or 0
        cote_pompe=self.cote_pompe.value or 0
        rest=float(cote_pompe) + float(prof_alter)
        self.temps_pompage.value=rest 
        self.temps_pompage.update()

    def openDatePicker(self,e):
        date=DatePicker(
            first_date=datetime(year=2000, month=10, day=1),
            last_date=datetime(year=2025, month=10, day=1),
            on_change=self.handle_change,
            on_dismiss=self.handle_dismissal,
        )
        self.page.open(date)

    def recupererDonnees(self):
        date_pompage = self.date_pompage.value
        type_pompe = self.type_pompe.value
        cote_pompe = self.cote_pompe.value
        temps_pompage = self.temps_pompage.value
        debit_pompage = self.debit_pompage.value
        niv_dynamique = self.niv_dynamique.value
        niv_statique = self.niv_statique.value
        observation = self.observation.value
        return {"date_pompage": date_pompage, "type_pompe": type_pompe,
                "cote_pompe": cote_pompe,"temps_pompage": temps_pompage, "debit_pompage": debit_pompage,
                "niv_dynamique": niv_dynamique, "niv_statique": niv_statique,
                "observation":observation
                }

    def SaveData(self, e):
        donnees = self.recupererDonnees()
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)

        try:
            c = conn.cursor()
            c.execute("""
                        UPDATE  pompage SET  date_pompage=?, type_pompe=?, cote_pompe=?, temps_pompage=?, debit_pompage=?, niv_dynamique=?, niv_statique=? observation=? WHERE id=?
                        """, (donnees["date_pompage"], donnees["type_pompe"], donnees["cote_pompe"],
                        donnees["temps_pompage"], donnees["debit_pompage"], donnees["niv_dynamique"], donnees["niv_statique"], donnees['observation'], self.donnees['id'])
                        )
            conn.commit()
        except Exception as e:
            print(e)
            return False
        self.formcontrol.updateData()
        self.formcontrol.close_dlg(e=None)

