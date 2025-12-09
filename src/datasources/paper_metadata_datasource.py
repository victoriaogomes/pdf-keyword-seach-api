from typing import List

from pymupdf import pymupdf

from datasources.clients.grobid_client import GrobidClient
from datasources.services.paper_service import PaperService
from entities.enums.paper_metadata import PaperMetadata


class PaperDatasource:

    def get_paper_metadata(self, folder_path: str, should_include_subfolders: bool, fields: List[PaperMetadata]):
        paper_list_metadata = []
        paper_list = PaperService.get_paper_list(folder_path, should_include_subfolders)

        for paper in paper_list:
            paper_info = {}
            paper_raw_metadata = GrobidClient.get_paper_metadata(paper)
            if PaperMetadata.TITLE in fields:
                paper_info["Title"] = paper_raw_metadata.get_title()
            if PaperMetadata.ABSTRACT in fields:
                paper_info["Abstract"] = paper_raw_metadata.get_abstract()
            if PaperMetadata.DOI in fields:
                paper_info["DOI"] = paper_raw_metadata.get_doi()
            if PaperMetadata.PAGE_COUNT in fields:
                paper_info["Page count"] = pymupdf.open(paper).page_count
            if PaperMetadata.AUTHORS in fields:
                paper_info["Authors"] = paper_raw_metadata.get_authors()
            if PaperMetadata.VENUE in fields:
                paper_info["Venue"] = paper_raw_metadata.get_venue()
            if PaperMetadata.PUBLICATION_YEAR in fields:
                paper_info["Publication Year"] = paper_raw_metadata.get_publication_year()
            paper_list_metadata.append(paper_info)

        return paper_list_metadata
