import json
from pathlib import Path
from typing import List

from openpyxl import Workbook

from configs.openpyxl.custom_worksheet import CustomWorksheet
from entities.paper_stats import PaperStats
from utils.constants import COUNT


class XlsxConverter:

    @staticmethod
    def to_xlsx(papers: List[PaperStats], output_path: str) -> None:
        path = Path(output_path) / "processed_papers.xlsx"
        paper_list = [paper.to_dict() for paper in papers]

        header = [COUNT, *paper_list[0].keys()]

        paper_list.sort(key=lambda x: x["filename"].lower())

        wb = Workbook()
        wb.remove(wb.active)

        worksheet = CustomWorksheet(wb.create_sheet())

        worksheet.add_header(header=header)

        for i, paper in enumerate(paper_list, start=1):
            paper["keyword_stats"] = json.dumps(paper["keyword_stats"])
            row = [i, *(paper[field] for field in paper.keys())]
            worksheet.add_row(row=row)

        worksheet.autofit_columns()

        worksheet.style_table(table_name="paper_list")

        wb.save(path)
        print("File saved!")
