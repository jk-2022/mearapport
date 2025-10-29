# weekly_report_view.py
from flet import *

from screens.rapportscreen.rapportcard import RapportCard
# from screens.rapportscreen.rapportform import RapportForm

from myaction import recuperer_liste_rapports


class RapportView(View):
    def __init__(self, page : Page,route:str="/rapport"):
        super().__init__()
        self.page=page
        self.projet=self.page.client_storage.get('projet')
        self.project_id = self.projet['id']
        self.project_name = self.projet['name']
        
        self.report_list = Column(
                    expand=1,
                    scroll=ScrollMode.ALWAYS,
                    )

        self.controls.append(
            SafeArea(
                Column(
                    controls=[
                        Row(
                            [
                            IconButton(icon=Icons.ARROW_BACK,on_click=self.page.on_view_pop),
                            Text(f"📁 Projet : {self.project_name}")
                            ]
                        ),
                        Row([
                            ElevatedButton("Filter",icon=Icons.SEARCH, on_click=self.goPlage),
                            ElevatedButton("Ajouter",icon=Icons.ADD, on_click=self.go_create_page),
                            ElevatedButton("Archives",icon=Icons.ARCHIVE, on_click=self.goArchive),
                            ],alignment=MainAxisAlignment.SPACE_BETWEEN
                            ),
                        Divider(),
                        Text("📋 Rapports journalier :"),
                        self.report_list
                    ]
                ),expand=1
            )
        )
        self.load_rapports()
        
    def load_rapports(self):
        self.report_list.controls.clear()
        rapports=recuperer_liste_rapports(self.projet["id"])
        if rapports:
            for rapport in rapports:
                des=['rid', 'title', 'content', 'rapport_date', 'created_at']
                rapport=dict(zip(des, rapport))
                self.report_list.controls.append(
                    RapportCard(page=self.page,rapport=rapport,formcontrol=self)
                )
      
        self.page.update()
        
    def go_create_page(self,e):
        self.page.go("/create-rapport")

    def goPlage(self,e):
        self.page.go("/plage")

    def goArchive(self,e):
        self.page.go("/archive")
    
    def close_dlg(self, e):
        self.page.close(self.dlg_modal)
        self.page.update()
