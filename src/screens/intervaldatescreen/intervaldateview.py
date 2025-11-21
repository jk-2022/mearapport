import datetime
from flet import *

from donnees import *
from myaction import found_ouvrage_interval
from .statdetailcontrol import StatDetailControl
from .statintervalcontrol import StatIntervalControl
from uix.custominputfield import CustomInputField

class IntervalDateView(View):
    def __init__(self, page : Page,route:str="/intervaldate"):
        super().__init__()
        self.page=page
            
        self.ouvrages_cont=Column(expand=True, scroll=ScrollMode.ALWAYS)
        
        self.date1=TextField(label='Date début',expand=True, on_click= self.show_date1,border_color=Colors.WHITE54 if self.page.theme_mode==ThemeMode.DARK else Colors.BLACK38)
        self.date2=TextField(label='Date début',expand=True, on_click= self.show_date2,border_color=Colors.WHITE54 if self.page.theme_mode==ThemeMode.DARK else Colors.BLACK38)
        
        self.btn_text=ElevatedButton('Afficher les resultats', on_click= self.show_result)
        self.detail_btn=TextButton('Voirs la liste des ouvrages', on_click=self.show_list_ouvrage)
        
        self.date_picker1=DatePicker(
                    first_date=datetime.datetime(year=2000, month=10, day=1),
                    on_change=self.handle_change1,
                )

        self.date_picker2=DatePicker(
                    first_date=datetime.datetime(year=2000, month=10, day=1),
                    on_change=self.handle_change2,
                )
        
        self.controls.append(
            SafeArea(
                Column(
                    controls=[
                        Row(
                            [
                            IconButton(icon=Icons.ARROW_BACK,on_click=self.page.on_view_pop),
                            Text(f"📁 Stastistiques par Intervall de date")
                            ]
                        ),
                        Row(
                            [
                            self.date1,
                            self.date2,
                            
                            ]
                        ),
                        self.btn_text,
                        self.ouvrages_cont
                    
                    ],
                    expand=True,
                    scroll=ScrollMode.ALWAYS
                )
                ,expand=True
            )
        )
        
    def handle_change1(self, e):
        self.date1.value=e.control.value.strftime('%Y-%m-%d')
        self.date1.update()

    def handle_change2(self, e):
        self.date2.value=e.control.value.strftime('%Y-%m-%d')
        self.date2.update()
        
    def show_date1(self,e):
        self.page.open(self.date_picker1)
    
    def show_date2(self,e):
        self.page.open(self.date_picker2)
        
    def show_result(self,e):
        date1=self.date1.value
        date2=self.date2.value
        self.result=found_ouvrage_interval(date1,date2)
        cont=StatIntervalControl(stats_data=self.result)
        self.ouvrages_cont.controls.append(cont)
        self.ouvrages_cont.controls.append(self.detail_btn)
        self.ouvrages_cont.update()
        
    def show_list_ouvrage(self,e):
        stat_details=self.result['details']
        cont=StatDetailControl(stats_data=stat_details)
        self.ouvrages_cont.controls.append(cont)
        self.detail_btn.visible=False
        self.detail_btn.update()
        self.ouvrages_cont.update()
