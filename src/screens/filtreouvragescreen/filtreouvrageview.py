from flet import *
import os
import csv
from allpath import AllPath
from myaction import get_all_localites, get_filtered_ouvrages, recuperer_one_local, recuperer_one_projet

from mystorage import *

path=AllPath()
path_data=path.path_data()

DB_PATH=os.path.join(path_data,"rapport.db")
ARCHIVES_PATH=path.path_generated_docs()


from .datatable import Mytable, tb

class FiltreOuvrageView(View):
    def __init__(self, page:Page,route:str="/filtrer-ouvrage"):
        super().__init__()
        self.page = page

        self.liste_ouvrage_filtrer=[]
        self.dropdown_type = Dropdown(
        label="Type",
        expand=True,
        border_color=Colors.WHITE54 if self.page.theme_mode==ThemeMode.DARK else Colors.BLACK54,
        text_size=13,
        options=[dropdown.Option("PMH"), dropdown.Option("PEA"), dropdown.Option("AEP"), dropdown.Option("PMH en PEA"), dropdown.Option("Mini AEP")],
        on_change=lambda e: self.update_list()
        )

        self.dropdown_etat = Dropdown(
            label="État",
            expand=True,
            border_color=Colors.WHITE54 if self.page.theme_mode==ThemeMode.DARK else Colors.BLACK54,
            text_size=12,
            options=[dropdown.Option("Bon état"), dropdown.Option("En panne"), dropdown.Option("Abandonné")],
            on_change=lambda e: self.update_list()
        )

        self.dropdown_localite_cnt=Container(
            expand=True
        )

        self.numero_irh = TextField(
            label="N° IRH", on_change=lambda e: self.update_list(),
            expand=True,
            border_color=Colors.WHITE54 if self.page.theme_mode==ThemeMode.DARK else Colors.BLACK54,
            text_size=12,
        )

        
        self.ouvrage_column_list = Column(
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
                            Text("Filtrer les ouvrages"),
                            ]
                        ),
                        Row(
                            [
                            self.dropdown_type,
                            self.dropdown_localite_cnt,
                            ],
                            alignment=MainAxisAlignment.SPACE_AROUND
                        ),
                        Row(
                            [
                            self.numero_irh,
                            self.dropdown_etat,
                            ],
                            alignment=MainAxisAlignment.SPACE_AROUND
                        ),
                    Divider(),
                    Mytable,
                    ElevatedButton("Générer CSV", on_click=self.showGenerate_csv),
                    ],spacing=7
                ), expand=True
            )
        )
        self.update_localite()

    def update_localite(self):
        localites=get_all_localites()
        self.dropdown_localite = Dropdown(
            label="Localite",
            expand=True,
            border_color=Colors.WHITE54 if self.page.theme_mode==ThemeMode.DARK else Colors.BLACK38,
            text_size=12,
            on_change=lambda e: self.update_list()
        )
        if localites:
            for localite in localites:
                self.dropdown_localite.options.append(dropdown.Option(localite[0]))
            self.dropdown_localite_cnt.content=self.dropdown_localite
        self.page.update()
    
    def update_list(self):
        self.ouvrage_column_list.controls.clear()
        projet=get_value('projet')
        projet_id=projet['id']
        ouvrages = get_filtered_ouvrages(
            type_ouvrage=self.dropdown_type.value,
            localite=self.dropdown_localite.value,
            etat=self.dropdown_etat.value,
            numero_irh=self.numero_irh.value,
            projet_id=projet_id
        )

        if ouvrages:
            # print(ouvrages)
            tb.rows = []
            self.liste_ouvrage_filtrer=[]
            for ouvrage in ouvrages:
                print(list(ouvrage.values()))
                self.liste_ouvrage_filtrer.append(list(ouvrage.values()))
                tb.rows.append(
                    DataRow(
                        cells=[
                            DataCell(Text(ouvrage["type_ouvrage"])),
                            DataCell(Text(ouvrage["numero_irh"])),
                            DataCell(Text(ouvrage["etat"])),
                            DataCell(Text(ouvrage["annee"])),
                            DataCell(Text(ouvrage["type_energie"])),
                            DataCell(Text(ouvrage["type_reservoir"])),
                            DataCell(Text(ouvrage["volume_reservoir"])),
                            DataCell(Text(ouvrage["cause_panne"])),
                            DataCell(Text(ouvrage["observation"])),
                        ],
                        data=ouvrage,
                        selected=True,
                        on_select_changed=lambda e, data=ouvrage: self.open_ouvrage_detail(data)
                    )
                )
            tb.update()
        else:
            tb.rows=[]
        self.page.update()

    def open_ouvrage_detail(self,ouvrage):
        projet=recuperer_one_projet(ouvrage['projet_id'])
        set_value('projet',projet[0])
        local=recuperer_one_local(ouvrage['localisation_id'])
        set_value('local',local[0])
        self.page.go("/recap-ouvrage")

    def showGenerate_csv(self,e):
        titlefield=TextField(expand=True, height=40)
        self.dlg_modal = AlertDialog(
            modal=True,
            title=Text("Nom du fichier"),
            content=titlefield,
            actions=[
                TextButton("Annuler", on_click=self.close_dlg),
                TextButton("Exporter", on_click = lambda e : self.generate_csv(titlefield.value)),
            ],
            actions_alignment= MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        self.page.open(self.dlg_modal)
        self.page.update()

    def generate_csv(self, filename):
        if filename=="":
            filename="Liste ouvrages"
        rows=self.liste_ouvrage_filtrer
        if rows:
            with open(f"{ARCHIVES_PATH}/{filename}.csv", mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file, delimiter=",")
                writer.writerow(["id","type_ouvrage", "prefecture", "commune", "canton", "localite", "numero irh", "coordonnee x", "coordonnee y",
                "lieu implantation","Année", "type energie", "type reservoir", "Vol reservoir",
                "etat", "cause_panne", "observation","created_at"])
                writer.writerows(rows)
            self.page.open(SnackBar(Text(f"{filename} saved successfuly"),open=True))
            self.close_dlg(e=None)
            return True
        self.page.open(SnackBar(Text(f"Error for vaving {filename}"),open=True))
    
    def close_dlg(self,e):
        self.page.close(self.dlg_modal)
        self.page.update()
            
