
# projets_view.py
from flet import *

from mystorage import *

from myaction import recuperer_liste_localisation_by_projet
from screens.localisationscreen.localform import LocalForm
from .localcard import LocalCard


class LocalisationView(View):
    def __init__(self,page:Page):
        super().__init__()
        self.padding = 0
        self.page=page
        self.projet=get_value('projet')
        self.localisation_list = Column(
            expand=True,
            scroll=ScrollMode.ALWAYS
        )
        self.searsh_button = ElevatedButton("Filter",icon=Icons.SEARCH, on_click=self.go_filter_page)
        self.add_button = ElevatedButton("Ajouter",icon=Icons.ADD, on_click=self.showNewLocal)
        # self.stat_button = ElevatedButton("Stast.",icon=Icons.AUTO_GRAPH_OUTLINED, on_click=self.go_static_page)

        self.controls.append(SafeArea(
            Column(
                controls=[
                    Container(
                        content=Row(
                                [
                                IconButton(icon=Icons.ARROW_BACK, on_click=self.page.on_view_pop),
                                Text("Tous ouvrages confondus ", text_align=TextAlign.CENTER)
                                ]
                                # ,alignment=MainAxisAlignment.CENTER
                            )
                    ),
                    # Divider(),
                    Container(
                        content=Row(
                            [
                                self.searsh_button,
                                self.add_button,
                                # self.stat_button,
                            ],alignment=MainAxisAlignment.SPACE_BETWEEN
                        ),
                        padding=padding.only(left=10, right=10)
                    ),
                    self.localisation_list
                        ],expand=True,scroll=ScrollMode.ALWAYS
                    ),expand=True
                )
            )
        self.load_localisations()

    def load_localisations(self):
        projet_id=self.projet['id']
        localisations=recuperer_liste_localisation_by_projet(projet_id)
        self.localisation_list.controls.clear()
        if localisations:
            for local in localisations:
                self.localisation_list.controls.append(
                LocalCard(page=self.page, local=local, projet=self.projet, formcontrol=self)
            )
        self.page.update()
    
    def showNewLocal(self,e):
        cont=LocalForm(page=self.page, projet=self.projet,formcontrol=self)
        self.dlg_modal = AlertDialog(
            modal=True,
            title=Text("Localisation Ouvrage"),
            content=cont,
            actions=[
                TextButton("Annuler", on_click=self.close_dlg),
                TextButton("Sauvegarder", on_click=cont.SaveData),
            ],
            actions_alignment= MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
            content_padding=0
        )
        self.page.open(self.dlg_modal)
        self.page.update()

    def go_filter_page(self,e):
        self.page.go("/filtrer-ouvrage")
        
    def close_dlg(self,e):
        self.page.close(self.dlg_modal)
        self.page.update()
    
    # def go_static_page(self,e):
    #     self.page.go("/statics")
