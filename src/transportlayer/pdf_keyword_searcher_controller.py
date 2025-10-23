from http import HTTPMethod

from fastapi import APIRouter, Body
from fastapi.params import Query
from kink import inject

from entities.enums.output_format import OutputFormat
from entities.enums.phase_status import PhaseStatus
from entities.search_keywords_request import SearchKeywordsRequest
from interactors.get_papers_by_venue_use_case import GetPapersByVenueUseCase
from interactors.search_keyword_use_case import SearchKeywordUseCase
from interactors.update_paper_status_use_case import UpdatePaperStatusUseCase


@inject
class PdfKeywordSearcherController:
    PATH_POST_SEARCH = "/search"
    PATH_GET_PAPERS = "/papers"
    PATH_POST_UPDATE = "/update"

    def __init__(self, search_keyword_use_case: SearchKeywordUseCase,
                 update_paper_status_use_case: UpdatePaperStatusUseCase,
                 get_papers_by_venue_use_case: GetPapersByVenueUseCase, api_router: APIRouter):
        self.get_papers_by_venue_use_case = get_papers_by_venue_use_case
        self.search_keyword_use_case = search_keyword_use_case
        self.update_paper_status_use_case = update_paper_status_use_case
        self.router = api_router
        self.__set_up_routes()

    def __set_up_routes(self):
        self.router.add_api_route(self.PATH_POST_SEARCH, self.search_keywords, methods=[HTTPMethod.POST])
        self.router.add_api_route(self.PATH_GET_PAPERS, self.get_papers, methods=[HTTPMethod.GET])
        self.router.add_api_route(self.PATH_POST_UPDATE, self.update_paper_status, methods=[HTTPMethod.POST])

    def search_keywords(self, search_keyword_request: SearchKeywordsRequest = Body(...)):
        self.search_keyword_use_case.execute(search_keyword_request)
        return {"message": search_keyword_request.pdf_folder_path}

    def get_papers(self,
                   phase_1_status: PhaseStatus | None = Query(None, description="Filter papers by phase 1 status"),
                   phase_2_status: PhaseStatus | None = Query(None, description="Filter papers by phase 2 status"),
                   fields: str = Query(None,
                                       description="Desired fields of the paper that must be present in the output"),
                   venue: str = Query(None, description="Filter papers by venue"),
                   output_format: OutputFormat = Query(OutputFormat.XLSX, description="Output format")):
        self.get_papers_by_venue_use_case.execute(venue, output_format, fields, phase_1_status, phase_2_status)
        return {"message": "success"}

    def update_paper_status(self, file_path: str = Query(None,
                                                         description="Path of the excel file that should be used to update the paper status"),
                            venue: str = Query(None, description="Venue to which the papers belong to")):
        self.update_paper_status_use_case.execute(file_path, venue)
