from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.worksheet.worksheet import Worksheet


class CustomWorksheet:
    CENTER = "center"
    WRAP_JUSTIFY_ALIGNMENT = Alignment(wrap_text=True, horizontal='justify', vertical=CENTER)
    WRAP_CENTER_ALIGNMENT = Alignment(wrap_text=True, horizontal=CENTER, vertical=CENTER)

    def __init__(self, worksheet: Worksheet):
        self.worksheet = worksheet

    def add_header(self, header: list[str], font_size: int = 12, bold: bool = True, vertical_alignment: str = CENTER,
                   horizontal_alignment: str = CENTER) -> None:
        font = Font(size=font_size, bold=bold)
        alignment = Alignment(wrap_text=True, horizontal=horizontal_alignment, vertical=vertical_alignment)

        self.worksheet.append(header)

        for col in range(1, len(header) + 1):
            self.worksheet.cell(row=1, column=col).font = font
            self.worksheet.cell(row=1, column=col).alignment = alignment

    def add_row(self, row, alignment=WRAP_JUSTIFY_ALIGNMENT) -> None:
        self.worksheet.append(row)

        for col in range(1, len(row) + 1):
            self.worksheet.cell(row=self.worksheet.max_row, column=col).alignment = alignment

    def autofit_columns(self):
        for col in self.worksheet.columns:
            max_length = 0
            column = col[0].column_letter
            for cell in col:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except TypeError:
                    # Must ignore cells with values that cannot be converted to string
                    # or whose length cannot be determined
                    pass
            adjusted_width = (max_length + 2)
            self.worksheet.column_dimensions[column].width = adjusted_width

    def style_table(self, table_name, first_row=1, style="TableStyleMedium2"):
        last_column_letter = get_column_letter(self.worksheet.max_column)
        tab = Table(displayName=table_name, ref=f"A{first_row}:{last_column_letter}{self.worksheet.max_row}")

        style = TableStyleInfo(
            name=style,
            showFirstColumn=False,
            showLastColumn=False,
            showRowStripes=True,
            showColumnStripes=False
        )
        tab.tableStyleInfo = style

        self.worksheet.add_table(tab)
