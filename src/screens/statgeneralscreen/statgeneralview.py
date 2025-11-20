from flet import *

from donnees import *
from mystorage import *
from .statanneecontrol import StatAnneeControl
from .statgeneralcontrol import StatGeneralControl
class StatGeneralView(View):
    def __init__(self, page : Page,route:str="/statgeneral"):
        super().__init__()
        self.page=page
        stats_gen= get_value('stats_gen')
        self.general_cnt=Column(expand=True, scroll=ScrollMode.ALWAYS)
        
        cont_gen=StatGeneralControl(page=self.page, stat_general=stats_gen)
        cont_ann=StatAnneeControl(page=self.page, stat_general=stats_gen)
        self.general_cnt.controls.append(cont_gen)
        self.general_cnt.controls.append(cont_ann)
        
        self.controls.append(
            SafeArea(
                Column(
                    controls=[
                        Row(
                            [
                            IconButton(icon=Icons.ARROW_BACK,on_click=self.page.on_view_pop),
                            Text(f"📁 Stastistiques Générals")
                            ]
                        ),
                        
                        self.general_cnt
                    
                    ],
                    expand=True,
                    scroll=ScrollMode.ALWAYS
                )
                ,expand=True
            )
        )
        
