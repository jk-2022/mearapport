from flet import *

tb_ouvrage = DataTable(
    columns=[
        DataColumn(Text("Type", weight="bold")),
        DataColumn(Text("Bon état", weight="bold")),
        DataColumn(Text("En panne", weight="bold")),
        DataColumn(Text("Abandonnée", weight="bold")),
        DataColumn(Text("Total", weight="bold")),
    ],
    rows=[],
    heading_row_color=Colors.BLUE_500,
    heading_row_height=40
)

Mytable_ouvrage = Column(
    scroll="auto",
    controls=[
        Row([tb_ouvrage], scroll="always")
    ]
)

# ===========================================

tb_detail_ouvrage = DataTable(
    columns=[
        DataColumn(Text("Type", weight="bold")),
        DataColumn(Text("Lieu", weight="bold")),
        DataColumn(Text("Canton", weight="bold")),
        DataColumn(Text("Commune", weight="bold")),
        DataColumn(Text("Etat", weight="bold")),
        DataColumn(Text("Annee", weight="bold")),
    ],
    rows=[],
    heading_row_color=Colors.BLUE_500,
    heading_row_height=40
)

Mytable_detail_ouvrage = Column(
    scroll="auto",
    controls=[
        Row([tb_detail_ouvrage], scroll="always")
    ]
)

# =======================================================

tb_annee = DataTable(
    columns=[
        DataColumn(Text("Type",weight="bold")),
        DataColumn(Text("Bon état", weight="bold")),
        DataColumn(Text("Panne", weight="bold")),
        DataColumn(Text("Abandonnée", weight="bold")),
        DataColumn(Text("Total", weight="bold"))
    ],
    rows=[],
    heading_row_color=Colors.ORANGE_500,
    heading_row_height=40
)

Mytable_annee = Column(
    scroll="auto",
    controls=[
        Row([tb_annee], scroll="always")
    ]
)