# projets_view.py
from flet import *
import sqlite3
import os

from allpath import AllPath

path=AllPath()
path_data=path.path_data()

DB_PATH=os.path.join(path_data,"rapport.db")


from myaction import recuperer_liste_projets
from screens.projetscreen.projetcard import ProjetCard
from screens.projetscreen.projetform import ProjetForm

class ProjectView(View):
    def __init__(self,page:Page,route:str="/project"):
        super().__init__()
        self.padding = 0
        self.page=page
        self.project_list = Column(expand=1,scroll=ScrollMode.ALWAYS)
        self.floating_action_button = FloatingActionButton(icon=Icons.ADD, on_click=self.show_projet)

        self.controls.append(SafeArea(
            Column(
                controls=[
                    Container(
                        content=Row(
                                [
                                IconButton(icon=Icons.ARROW_BACK, on_click=self.page.on_view_pop),
                                Text("Liste des projets ", text_align=TextAlign.CENTER)
                                ]
                                # ,alignment=MainAxisAlignment.CENTER
                            ),
                            # alignment=alignment.center,
                    ),
                    Container(
                        padding=padding.only(right=20),
                        content=Row(
                        [
                            ElevatedButton("Statistiques", on_click= self.go_to_static, icon=Icons.STACKED_LINE_CHART_OUTLINED)
                        ],alignment=MainAxisAlignment.END
                    )
                    ),
                    self.project_list
                        ],expand=True,scroll=ScrollMode.ALWAYS
                    ),expand=True
                )
            )
        self.load_projects()
    
    def load_projects(self):
        self.project_list.controls.clear()
        projets=recuperer_liste_projets()
        if projets:
            for projet in projets:
                self.project_list.controls.append(
                ProjetCard(page=self.page, projet=projet,formcontrol=self)
            )
        
    def show_projet(self,e):
        projet_content = ProjetForm(self.page, self)
        self.dlg_modal = AlertDialog(
            modal=True,
            title=Text("Nouveau projet"),
            content=projet_content,
            actions=[
                TextButton("Annuler", on_click=self.close_dlg),
                TextButton("Enregistrer", on_click=projet_content.SaveData),
            ],
            actions_alignment= MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
            content_padding=0
        )
        self.page.open(self.dlg_modal)
        self.page.update()
        
    def go_to_static(self, e):
        self.page.go("/stats")
        # self.page.go("/statics")
        
    def close_dlg(self, e):
        self.page.close(self.dlg_modal)
        self.page.update()
