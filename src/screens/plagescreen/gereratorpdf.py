from fpdf import FPDF
from fpdf.enums import XPos, YPos

class GeneratorPDF(FPDF):
    def __init__(self,rappor_title):
        super().__init__()
        self.rappor_title=rappor_title

    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, f"{self.rappor_title}", border=False, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        self.ln(5)

    def table_row(self, report, col_widths):
        x, y = self.get_x(), self.get_y()

        # Calcule la hauteur requise par la cellule "Contenu"
        contenu_lines = self.multi_cell(col_widths[2], self.font_size + 2, report['content'], dry_run=True, output="LINES")
        row_height = len(contenu_lines) * (self.font_size + 2)

        # --- DATE ---
        self.set_xy(x, y)
        self.rect(x, y, col_widths[0], row_height)  # encadré de la cellule
        self.multi_cell(col_widths[0], self.font_size + 2, report['rapport_date'], border=0, align='L')

        # --- TITRE ---
        x_titre = x + col_widths[0]
        self.set_xy(x_titre, y)
        self.rect(x_titre, y, col_widths[1], row_height)
        self.multi_cell(col_widths[1], self.font_size + 2, report['title'].upper(), border=0, align='L')

        # --- CONTENU ---
        x_contenu = x_titre + col_widths[1]
        self.set_xy(x_contenu, y)
        self.multi_cell(col_widths[2], self.font_size + 2, report['content'], border=1, align='L')

        # Repositionne le curseur pour la ligne suivante
        self.set_y(y + row_height)




