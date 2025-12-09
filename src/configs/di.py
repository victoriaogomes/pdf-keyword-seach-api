from fastapi import APIRouter
from kink import di

from datasources.paper_metadata_datasource import PaperDatasource
from datasources.paper_keyword_searcher import PaperKeywordSearcher
from interactors.get_paper_metadata_use_case import GetPaperMetadataUseCase
from interactors.search_keyword_use_case import SearchKeywordUseCase


class Di:
    @staticmethod
    def set_up():
        di[APIRouter] = APIRouter()
        di[PaperKeywordSearcher] = PaperKeywordSearcher()
        di[PaperDatasource] = PaperDatasource()
        di[SearchKeywordUseCase] = SearchKeywordUseCase()
        di[GetPaperMetadataUseCase] = GetPaperMetadataUseCase()