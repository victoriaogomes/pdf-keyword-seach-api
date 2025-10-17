from fastapi import APIRouter, Body
from kink import inject

from entities.search_keywords_request import SearchKeywordsRequest
from interactors.search_keyword_use_case import SearchKeywordUseCase


@inject
class PdfKeywordSearcherController:

    def __init__(self, search_keyword_use_case: SearchKeywordUseCase, api_router: APIRouter):
        self.search_keyword_use_case = search_keyword_use_case
        self.router = api_router
        self.__set_up_routes()

    def __set_up_routes(self):
        self.router.add_api_route("/search", self.search_keywords, methods=["POST"])

    # @staticmethod
    # @router.post("/search")
    def search_keywords(self, search_keyword_request: SearchKeywordsRequest = Body(...)):
        self.search_keyword_use_case.execute(search_keyword_request)
        return {"message": search_keyword_request.pdf_folder_path}
