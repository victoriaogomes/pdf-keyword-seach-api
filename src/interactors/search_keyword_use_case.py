from kink import inject

from datasources.paper_keyword_searcher import PaperKeywordSearcher
from datasources.paper_stats_datasource import PaperStatsDataSource
from entities.search_keywords_request import SearchKeywordsRequest


@inject
class SearchKeywordUseCase:

    def __init__(self, paper_keyword_searcher: PaperKeywordSearcher, paper_stats_data_source: PaperStatsDataSource):
        self.paper_keyword_searcher = paper_keyword_searcher
        self.paper_stats_data_source = paper_stats_data_source

    def execute(self, search_keyword_request: SearchKeywordsRequest):
        results = self.paper_keyword_searcher.analyze_papers_in_path(
            search_keyword_request.pdf_folder_path,
            search_keyword_request.keywords,
            search_keyword_request.include_subfolders,
            search_keyword_request.ignore_reference_section,
            search_keyword_request.output_path)

        self.paper_stats_data_source.save_all(results)
