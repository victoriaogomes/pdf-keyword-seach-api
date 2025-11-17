from http import HTTPMethod

from fastapi import APIRouter, Body, HTTPException
from kink import inject

from entities.search_keywords_request import SearchKeywordsRequest
from interactors.exceptions.no_pdf_found_exception import NoPdfFoundException
from interactors.search_keyword_use_case import SearchKeywordUseCase


@inject
class PdfKeywordSearcherController:
    PATH_POST_SEARCH = "/search"

    def __init__(self, search_keyword_use_case: SearchKeywordUseCase, api_router: APIRouter):
        self.search_keyword_use_case = search_keyword_use_case
        self.router = api_router
        self.__set_up_routes()

    def __set_up_routes(self):
        self.router.add_api_route(self.PATH_POST_SEARCH, self.search_keywords, methods=[HTTPMethod.POST])

    def search_keywords(self, search_keyword_request: SearchKeywordsRequest = Body(...)):
        try:
            self.search_keyword_use_case.execute(search_keyword_request)
            return {"message": "PDF files successfully processed",
                    "output_path": search_keyword_request.output_path}
        except NoPdfFoundException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
