from fastapi import APIRouter
from kink import di

from configs.db.mongodb_client import MongoDBClient
from datasources.paper_keyword_searcher import PdfKeywordSearcher
from datasources.paper_stats_datasource import PaperStatsDataSource
from interactors.search_keyword_use_case import SearchKeywordUseCase
from configs.document.paper_stats_document import PaperStatsDocument


class Di:
    @staticmethod
    def set_up():
        di[APIRouter] = APIRouter()
        di[MongoDBClient] = MongoDBClient()
        di[PaperStatsDataSource] = PaperStatsDataSource()
        di[PdfKeywordSearcher] = PdfKeywordSearcher()
        di[SearchKeywordUseCase] = SearchKeywordUseCase()