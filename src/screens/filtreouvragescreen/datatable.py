from flet import *

tb = DataTable(
    columns=[
        DataColumn(Text("Type",weight="bold", size=12)),
        # DataColumn(Text("Prefecture", weight="bold", size=12)),
        # DataColumn(Text("Commune", weight="bold", size=12)),
        # DataColumn(Text("Canton", weight="bold", size=12)),
        # DataColumn(Text("Localite",weight="bold", size=12)),
        DataColumn(Text("N° Irh",weight="bold", size=12)),
        DataColumn(Text("Etat", weight="bold", size=12)),
        # DataColumn(Text("Lieu", weight="bold", size=12)),
        DataColumn(Text("Année", weight="bold", size=12)),
        # DataColumn(Text("Coord. X", weight="bold", size=12)),
        # DataColumn(Text("Coord. Y", weight="bold", size=12)),
        DataColumn(Text("Type energie", weight="bold", size=12)),
        DataColumn(Text("Type reservoir", weight="bold", size=12)),
        DataColumn(Text("Vol. reserv.", weight="bold", size=12)),
        DataColumn(Text("Causes", weight="bold", size=12)),
        DataColumn(Text("Observation", weight="bold", size=12)),
        # DataColumn(Text("Date", weight="bold", size=12)),
    ],
    rows=[]
)

Mytable = Column(
    scroll="auto",
    controls=[
        Row([tb], scroll="always")
    ]
)
