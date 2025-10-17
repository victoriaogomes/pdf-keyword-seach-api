from typing import List

from kink import inject

from datasources.paper_keyword_searcher import PdfKeywordSearcher
from entities.paper_stats import PaperStats
from entities.search_keywords_request import SearchKeywordsRequest
from utils.json_converter import JsonConverter


@inject
class SearchKeywordUseCase:

    def __init__(self, pdf_keyword_searcher: PdfKeywordSearcher):
        self.pdf_keyword_searcher = pdf_keyword_searcher

    def execute(self, search_keyword_request: SearchKeywordsRequest):
        pdf_stats_list: List[PaperStats] = self.pdf_keyword_searcher.analyze_papers_in_path(
            search_keyword_request.pdf_folder_path,
            search_keyword_request.keywords,
            search_keyword_request.should_include_subfolders,
            search_keyword_request.should_ignore_reference_section,
            search_keyword_request.output_path)

        JsonConverter.pdf_stats_list_to_json(pdf_stats_list)
        JsonConverter.pdf_stats_list_to_ndjson(pdf_stats_list)
