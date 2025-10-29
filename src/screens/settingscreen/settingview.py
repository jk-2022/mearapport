from flet import *
from myaction import export_sqlite_to_json, import_json_to_sqlite
from mystorage import *

class SettingView(View):
    def __init__(self,page:Page, route:str="/settings"):
        super().__init__()
        self.padding = 0
        self.page=page

        self.pick_files_dialog = FilePicker(on_result=self.pick_files_result)
        self.page.overlay.append(self.pick_files_dialog)
       
        self.controls.append(SafeArea(
            Column(
                controls=[
                    Container(
                        content=Row(
                                [
                                IconButton(icon=Icons.ARROW_BACK, on_click=self.page.on_view_pop),
                                Text("Paramètres ", text_align=TextAlign.CENTER)
                                ]
                            )
                    ),
                    Container(
                        padding=padding.only(right=10),
                        content=Row([
                        Text("Gestions des données", italic=True,size=11)
                        ],alignment=MainAxisAlignment.END
                        ),
                    ),
                    Card(
                        content=Container(
                            padding=10,
                            content=Column(
                                [
                                    
                                    ListTile(title=Text("Sauvegardez toutes vos données"),leading=Icon(Icons.UPLOAD), on_click=self.showExport),
                                    ListTile(title=Text("Importez toutes vos données"),leading=Icon(Icons.DOWNLOAD), on_click=lambda _: self.pick_files_dialog.pick_files(allowed_extensions=["json"]))
                                ]
                            )
                        )
                    ),
                    Container(
                        padding=padding.only(right=10,top=20),
                        content=Row([
                        Text("thème", italic=True,size=11)
                        ],alignment=MainAxisAlignment.END
                        ),
                    ),
                    Card(
                        content=Container(
                            content=Row(
                                [
                                    Text("Changer le mode de thème"),
                                    Switch(label='',label_position=LabelPosition.LEFT,on_change=self.togle_theme)
                                ],alignment=MainAxisAlignment.SPACE_BETWEEN
                            ),
                            padding=padding.only(left=10,right=20)
                        )
                    )
                ],expand=True,spacing=0
            ),expand=True
        )
    )
        
    def showExport(self,e):
        titlefield=TextField(expand=True, height=40,value="basedb")
        self.dlg_modal = AlertDialog(
            modal=True,
            title=Text("Nom du fichier"),
            content=titlefield,
            actions=[
                TextButton("Annuler", on_click=self.close_dlg),
                TextButton("Exporter", on_click = lambda e : self.export_base(titlefield.value)),
            ],
            actions_alignment= MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        self.page.open(self.dlg_modal)
        self.page.update()

    def pick_files_result(self,e: FilePickerResultEvent):
        file_path = e.files[0].path
        file_name = (", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!")
        file_name=file_name.split("_")
        file_name=file_name[0]
        import_json_to_sqlite(file_path)
        self.page.open(SnackBar(Text(f"Importation avec succès")))
        
    def export_base(self,title):
        export_sqlite_to_json(title)
        self.close_dlg(e=None)
        self.page.open(SnackBar(Text(f"La sauvegarde {title} est exporter avec succès")))

    # def import_base(self,e):
    #     export_sqlite_to_json("text")

    def togle_theme(self,e):
        if self.page.theme_mode == ThemeMode.DARK : 
            self.page.theme_mode=ThemeMode.LIGHT
            set_value('theme','ThemeMode.LIGHT')
        else:
            self.page.theme_mode=ThemeMode.DARK
            set_value('theme','ThemeMode.DARK')
        self.page.update()

    def close_dlg(self,e):
        self.page.close(self.dlg_modal)
        self.page.update()
