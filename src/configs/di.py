from fastapi import APIRouter
from kink import di

from datasources.clients.mongodb_client import MongoDBClient
from configs.env.env_settings import EnvSettings
from datasources.clients.open_search_client import OpenSearchClient
from datasources.open_search_datasource import OpenSearchDatasource
from datasources.paper_keyword_searcher import PaperKeywordSearcher
from datasources.paper_stats_datasource import PaperStatsDataSource
from interactors.get_papers_by_venue_use_case import GetPapersByVenueUseCase
from interactors.search_keyword_use_case import SearchKeywordUseCase
from interactors.update_paper_status_use_case import UpdatePaperStatusUseCase


class Di:
    @staticmethod
    def set_up():
        di[EnvSettings] = EnvSettings()
        di[APIRouter] = APIRouter()
        di[MongoDBClient] = MongoDBClient()
        di[OpenSearchClient] = OpenSearchClient()
        di[PaperStatsDataSource] = PaperStatsDataSource()
        di[PaperKeywordSearcher] = PaperKeywordSearcher()
        di[SearchKeywordUseCase] = SearchKeywordUseCase()
        di[GetPapersByVenueUseCase] = GetPapersByVenueUseCase()
        di[UpdatePaperStatusUseCase] = UpdatePaperStatusUseCase()
        di[OpenSearchDatasource] = OpenSearchDatasource()