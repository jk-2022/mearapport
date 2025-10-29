import os
from flet import *
from fpdf import FPDF
from docx import Document
import csv
import sqlite3
import json

from allpath import AllPath

path=AllPath()
path_data=path.path_data()
generated_docs=path.path_generated_docs()

DB_PATH=os.path.join(path_data,"rapport.db")

from screens.rapportscreen.rapportupdateform import RapportUpdateForm

class PlageRapportCard(Card):
    def __init__(self, page: Page, rapport, formcontrol):
        super().__init__()
        self.page=page
        self.expand=True
        self.elevation=10
        self.rapport=rapport
        self.formcontrol=formcontrol
        self.contenue_cont=Column(
                            controls=[
                                Text(f"📝 {rapport['title']}"),
                                Text(f"Rapport du {rapport['rapport_date']}"), 
                            ],expand=True
                            )
        
                            
            
        self.content=Container(
            padding=padding.all(10),
            data=rapport,
            ink=True,
            expand=True,
            content=Container(
                content=Column(
                    [
                        self.contenue_cont,
                        ]
                    ),
                padding=10,
                expand=True
            )
        )
        self.convertir_bd_content(rapport['content'])

    def convertir_bd_content(self, cont):
        content=json.loads(cont)
        info=content.pop("info_ouvrage")
        type_ouvrage=content.pop("type_ouvrage")
        if type_ouvrage:
            text_info=""
            for key,value in info.items():
                if value=="":
                    text_info=text_info
                else:
                    text_info +=f"{key} : {value}   "
            if text_info!="":
                text=Text(f">> {type_ouvrage}\n ",size=13,spans=[TextSpan(f"{text_info}",
                                        TextStyle( size=11,italic=True, weight=FontWeight.W_200)
                                        )
                                        ])
                self.contenue_cont.controls.append(text)

        for key,value in content.items():
            texte=Text(f">> {key.upper()}\n ",size=13,spans=[TextSpan(f"{value}",
                                       TextStyle( size=11,italic=True, weight=FontWeight.W_200)
                                       )
                                    ])
            self.contenue_cont.controls.append(texte)
        
