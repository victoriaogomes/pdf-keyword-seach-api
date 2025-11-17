from fastapi import APIRouter
from kink import di

from datasources.paper_keyword_searcher import PaperKeywordSearcher
from interactors.search_keyword_use_case import SearchKeywordUseCase


class Di:
    @staticmethod
    def set_up():
        di[APIRouter] = APIRouter()
        di[PaperKeywordSearcher] = PaperKeywordSearcher()
        di[SearchKeywordUseCase] = SearchKeywordUseCase()