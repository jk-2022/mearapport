import json
from flet import *
import sqlite3
import os
from allpath import AllPath
from .plagerapportcard import PlageRapportCard

path=AllPath()
path_data=path.path_data()

DB_PATH=os.path.join(path_data,"rapport.db")
ARCHIVES_PATH=path.path_generated_docs()


from .gereratorpdf import GeneratorPDF
from .generatordocx import GeneratorDOCX
class PlageView(View):
    def __init__(self, page:Page,route:str="/plage"):
        super().__init__()
        self.page = page
        self.projet=self.page.data["projet"]
        self.projet_id = self.projet["id"]
        self.repports_list=[]

        self.start_date_dropdown = Dropdown(label="Date début",expand=True, border_color=Colors.WHITE54,text_size=10, on_change=lambda e: self.filter_reports())
        self.end_date_dropdown = Dropdown(label="Date fin",expand=True, border_color=Colors.WHITE54,text_size=10, on_change=lambda e: self.filter_reports())


        self.report_list_cont = Column(
            expand=1,
            scroll=ScrollMode.ALWAYS
        )

        self.controls.append(
            SafeArea(
                Column(
                    [
                    Row(
                        [
                        IconButton(icon=Icons.ARROW_BACK, on_click=self.page.on_view_pop),
                        Text("Filtrer les rapports par période")
                        ]
                    ),
                    Container(
                        # expand=True,
                        content=Row(
                            [
                            self.start_date_dropdown,
                            self.end_date_dropdown,
                            ],
                            alignment=MainAxisAlignment.SPACE_AROUND
                        )
                    ),
                    Divider(),
                    self.report_list_cont,
                    Row(
                        [
                            ElevatedButton("Générer PDF", on_click=self.generate_pdf),
                            ElevatedButton("Générer DOCX", on_click=self.generate_docx),
                        ],alignment=MainAxisAlignment.SPACE_EVENLY
                    )
                    ]
                ), expand=True
            )
        )

        self.load_available_dates()

    def load_available_dates(self):
        """Charge toutes les dates disponibles dans la base pour ce projet"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT DISTINCT rapport_date
            FROM rapports
            WHERE projet_id = ?
            ORDER BY rapport_date ASC
            """,
            (self.projet_id,)
        )
        dates = [row[0] for row in cursor.fetchall()]
        conn.close()

        if dates:
            self.start_date_dropdown.options = [dropdown.Option(date) for date in dates]
            self.end_date_dropdown.options = [dropdown.Option(date) for date in dates]
            self.page.update()

    def filter_reports(self):
        
        start = self.start_date_dropdown.value
        end = self.end_date_dropdown.value

        if not start or not end:
            self.report_list_cont.controls.append(Text("Veuillez choisir une date de début et de fin."))
            self.page.update()
            return

        # Vérification que la date de début est avant ou égale à la date de fin
        if start > end:
            self.report_list_cont.controls.append(Text("⚠️ La date de début doit précéder la date de fin."))
            self.page.update()
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT title, content, rapport_date
            FROM rapports
            WHERE projet_id = ? AND rapport_date BETWEEN ? AND ?
            ORDER BY rapport_date DESC
            """,
            (self.projet_id, start, end)
        )
        reports = cursor.fetchall()
        conn.close()
        # print(reports)
        if reports:
            self.report_list_cont.controls.clear()
            self.repports_list=[]
            for report in reports:
                des=["title", "content", "rapport_date"]
                rep=dict(zip(des, report))
                self.repports_list.append(rep)
        if not reports:
            self.report_list_cont.controls.append(Text("Aucun rapport trouvé pour cette période."))
        else:
            for rapport in self.repports_list:
                pass
                self.report_list_cont.controls.append(
                    PlageRapportCard(page=self.page,rapport=rapport,formcontrol=self)
                )
        self.page.update()

    def generate_docx(self, e):
        start = self.start_date_dropdown.value
        end = self.end_date_dropdown.value
        reports=self.repports_list
        # print(reports)
        if not reports:
            self.dialog = AlertDialog(
                title=Text("Aucun rapport trouvé.")
                )
            self.page.open(self.dialog)
            self.page.update()
            return

        # Sauvegarde du PDF
        output_dir = f"{ARCHIVES_PATH}"
        rapport_title=f"Rapports du {start} au {end}"
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{output_dir}/{rapport_title}.docx"

        # Création du DOCX
        docx = GeneratorDOCX(donnees=reports,titre=rapport_title,filename=filename)
        docx.create_docx()


        self.page.open(SnackBar(Text(f"✅ PDF généré avec succès : {filename}")))
        self.page.update()

        return self.repports_list
    
    def generate_pdf(self, e):
        start = self.start_date_dropdown.value
        end = self.end_date_dropdown.value
        reports=self.repports_list
        if not reports:
            self.dialog = AlertDialog(
                title=Text("Aucun rapport trouvé.")
                )
            self.page.open(self.dialog)
            self.page.update()
            return

        # Création du PDF
        rapport_title=f"Rapports du {start} au {end}"
        pdf = GeneratorPDF(rappor_title=rapport_title)
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Helvetica", size=12)

        # Largeurs des colonnes
        col_widths = [30, 40, 120]

        # En-têtes du tableau
        headers = ["Date", "Titre", "Activités"]
        for i in range(len(headers)):
            pdf.cell(col_widths[i], 10, headers[i], border=1, align="C")
        pdf.ln()

        # Données
        for report in reports:
            content=json.loads(report['content'])
            info=content.pop("info_ouvrage")
            type_ouvrage=content.pop("type_ouvrage")
            text_info=""
            text_cont=""
            if type_ouvrage:
                text_info+=f">Type Ouvrage : {type_ouvrage}\n"
                for key,value in info.items():
                    if value=="":
                        text_info=text_info
                    else:
                        text_info +=f"{key} : {value}   "
                

            for key,value in content.items():
                texte=Text(f"> {key.upper()}\n {value}")
                text_cont += f"{texte.value}\n"
            
            text_final=""
            if text_info!="":
                text_final= f"{text_info}\n{text_cont}"
            else:
                text_final=text_cont

            report['content']=text_final
            pdf.table_row(report, col_widths)

        # Sauvegarde du PDF
        output_dir = f"{ARCHIVES_PATH}"
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{output_dir}/{rapport_title}.pdf"
        pdf.output(filename)

        self.page.open(SnackBar(Text(f"✅ PDF généré avec succès : {filename}")))
        self.page.update()
        return self.repports_list

