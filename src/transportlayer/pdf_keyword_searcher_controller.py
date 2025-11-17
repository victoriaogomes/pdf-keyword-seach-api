from http import HTTPMethod

from fastapi import APIRouter, Body
from kink import inject

from entities.search_keywords_request import SearchKeywordsRequest
from interactors.search_keyword_use_case import SearchKeywordUseCase


@inject
class PdfKeywordSearcherController:
    PATH_POST_SEARCH = "/search"
    PATH_GET_PAPERS = "/papers"
    PATH_POST_UPDATE = "/update"

    def __init__(self, search_keyword_use_case: SearchKeywordUseCase, api_router: APIRouter):
        self.search_keyword_use_case = search_keyword_use_case
        self.router = api_router
        self.__set_up_routes()

    def __set_up_routes(self):
        self.router.add_api_route(self.PATH_POST_SEARCH, self.search_keywords, methods=[HTTPMethod.POST])

    def search_keywords(self, search_keyword_request: SearchKeywordsRequest = Body(...)):
        self.search_keyword_use_case.execute(search_keyword_request)
        return {"message": search_keyword_request.pdf_folder_path}
