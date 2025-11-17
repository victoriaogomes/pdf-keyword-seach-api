from typing import List

from dotmap import DotMap
from openpyxl import Workbook

from configs.openpyxl.custom_worksheet import CustomWorksheet
from utils.constants import COUNT


class XlsxConverter:

    @staticmethod
    def to_xlsx(paper_list: List[DotMap], venue: str, fields: List[str]) -> None:
        header = [COUNT, *fields]

        paper_list.sort(key=lambda x: x.filename.lower())

        wb = Workbook()
        wb.remove(wb.active)

        # Creates a new tab with the conference name
        worksheet = CustomWorksheet(wb.create_sheet())

        # Adds worksheet header
        worksheet.add_header(header=header)

        worksheet.redimension_columns(
            {
                "A": 10,  # Counter
                "B": 30,  # Id
                "C": 130  # title
            }
        )

        for i, paper in enumerate(paper_list, start=1):
            row = [i, str(paper._id), paper.filename.rstrip(".pdf"), paper.keywords_total]
            worksheet.add_row(row=row)

        worksheet.style_table(table_name=venue)

        # Salva arquivo
        wb.save(f"papers_from_{venue}.xlsx")
        print("File saved!")
