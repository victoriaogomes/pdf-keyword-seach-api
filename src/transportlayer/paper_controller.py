from http import HTTPMethod

from fastapi import APIRouter, Body, HTTPException, Query
from kink import inject

from entities.search_keywords_request import SearchKeywordsRequest
from interactors.exceptions.no_pdf_found_exception import NoPdfFoundException
from interactors.get_paper_metadata_use_case import GetPaperMetadataUseCase
from interactors.search_keyword_use_case import SearchKeywordUseCase


@inject
class PaperController:
    PATH_POST_SEARCH = "/search"
    PATH_GET_PAPER_METADATA = "/paper/metadata"

    def __init__(self, get_paper_metadata_use_case: GetPaperMetadataUseCase,
                 search_keyword_use_case: SearchKeywordUseCase, api_router: APIRouter):
        self.get_paper_metadata_use_case = get_paper_metadata_use_case
        self.search_keyword_use_case = search_keyword_use_case
        self.router = api_router
        self.__set_up_routes()

    def __set_up_routes(self):
        self.router.add_api_route(self.PATH_POST_SEARCH, self.search_keywords, methods=[HTTPMethod.POST])
        self.router.add_api_route(self.PATH_GET_PAPER_METADATA, self.get_paper_metadata, methods=[HTTPMethod.GET])

    def search_keywords(self, search_keyword_request: SearchKeywordsRequest = Body(...)):
        try:
            self.search_keyword_use_case.execute(search_keyword_request)
            return {"message": "PDF files successfully processed",
                    "output_path": search_keyword_request.output_path}
        except NoPdfFoundException as e:
            raise HTTPException(status_code=e.code, detail=e.message)

    def get_paper_metadata(self,
                           folder_path: str = Query(None,
                                                    description="Path where the papers that must be processed are stored"),
                           # should_include_subfolders: bool = Query(True,
                           #                                         description="Informs if we must consider the files in the subfolders of the received folder path"),
                           # fields: str | None = Query(None,
                           #                            description="List of metadata fields that must be returned")
                           ):
        try:
            # self.get_paper_metadata_use_case.execute(folder_path, should_include_subfolders, fields)
            self.get_paper_metadata_use_case.execute(folder_path, True, None)
            return {"message": "PDF files successfully processed"}
        except NoPdfFoundException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
