from typing import List

from kink import inject

from datasources.paper_keyword_searcher import PaperKeywordSearcher
from entities.enums.output_format import OutputFormat
from entities.paper_stats import PaperStats
from entities.search_keywords_request import SearchKeywordsRequest
from interactors.exceptions.no_pdf_found_exception import NoPdfFoundException
from utils.json_converter import JsonConverter
from utils.xlsx_converter import XlsxConverter


@inject
class SearchKeywordUseCase:
    NO_PDF_FOUND_ERROR = "No PDF file found for processing in the received folder path"

    def __init__(self, paper_keyword_searcher: PaperKeywordSearcher):
        self.paper_keyword_searcher = paper_keyword_searcher

    def execute(self, search_keyword_request: SearchKeywordsRequest):
        results: List[PaperStats] = self.paper_keyword_searcher.analyze_papers_in_path(
            search_keyword_request.pdf_folder_path,
            search_keyword_request.keywords,
            search_keyword_request.include_subfolders,
            search_keyword_request.ignore_reference_section,
            search_keyword_request.output_path)

        if results:
            if search_keyword_request.output_format == OutputFormat.XLSX:
                XlsxConverter.to_xlsx(papers=results, output_path=search_keyword_request.output_path)
            elif search_keyword_request.output_format == OutputFormat.JSON:
                JsonConverter.to_json(papers=results, output_path=search_keyword_request.output_path)
        else:
            raise NoPdfFoundException(message=self.NO_PDF_FOUND_ERROR, code=400)
