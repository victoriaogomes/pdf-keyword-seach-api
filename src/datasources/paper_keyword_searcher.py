import re
from pathlib import Path
from typing import List

from kink import inject
from pymupdf import Document, Page

from datasources.models.paper_stats_document import PaperStatsDocument
from entities.keyword_stats import KeywordStats
from entities.paper_stats import PaperStats


@inject
class PaperKeywordSearcher:
    PDF_EXTENSION = "*.pdf"
    REFERENCE_KEYWORDS = ["references", "bibliography"]
    REFERENCE_PATTERN = re.compile(
        r'^\s*(?:(?:\d+|[IVXLCDM]+)\.\s*)?(?:' + "|".join(REFERENCE_KEYWORDS) + r')\b',
        re.IGNORECASE
    )

    LOG_AMOUNT_OF_PAPERS_TO_PROCESS = "There are {} papers to process in the chosen folder."
    LOG_STEP_UPDATE = "Finished processing paper {}/{}: {}"
    TEXT = "text"

    def analyze_papers_in_path(self, path: str, keywords: List[str], should_include_subfolders: bool,
                               should_ignore_reference_section: bool, output_path: str) -> List[PaperStats]:
        results = []
        papers_to_process = self.__get_paper_list(path, should_include_subfolders)
        print(self.LOG_AMOUNT_OF_PAPERS_TO_PROCESS.format(len(papers_to_process)))

        for index, pdf_file_path in enumerate(papers_to_process):
            results.append(self.__search_for_keywords_in_paper(pdf_file_path, keywords,
                                                               should_ignore_reference_section, output_path))
            print(self.LOG_STEP_UPDATE.format(index + 1, len(papers_to_process), pdf_file_path))

        return results

    def __get_paper_list(self, folder_path: str, should_include_subfolders: bool):
        folder = Path(folder_path)
        if should_include_subfolders:
            return list(folder.rglob(self.PDF_EXTENSION))
        else:
            return list(folder.glob(self.PDF_EXTENSION))

    def __search_for_keywords_in_paper(self, pdf_file_path: Path, keywords: List[str],
                                       should_ignore_reference_section: bool, output_path: str) -> PaperStats:
        paper_stats_doc: PaperStatsDocument = PaperStatsDocument(pdf_file_path)

        keyword_regex_dict = {
            keyword: re.compile(r'\b(?:' + keyword + r')(?=\d|\b|[^a-zA-Z])', re.IGNORECASE)
            for keyword in keywords
        }

        margin = 10

        results = {kw: KeywordStats(kw) for kw in keywords}

        ref_coordinate, ref_page_number = self.get_references_page_and_coordinate(paper_stats_doc.get_doc())

        for page in paper_stats_doc.get_doc():
            page_number = page.number + 1
            for keyword in keywords:
                keywords_coordinates = page.search_for(keyword)
                for coord in keywords_coordinates:
                    if should_ignore_reference_section and self.is_in_ref_section(coord, ref_coordinate, page,
                                                                                  ref_page_number, page_number):
                        continue

                    expanded_rect = coord + (-margin, -margin, margin, margin)
                    found_text = page.get_textbox(expanded_rect)

                    if keyword_regex_dict[keyword].findall(found_text):
                        results[keyword].add_occurrence(page_number)
                        paper_stats_doc.increase_keyword_total_count(1)
                        paper_stats_doc.add_toc_entry(keyword=keyword, page_number=page_number)
                        paper_stats_doc.highlight_keyword(page=page, instance=coord, keyword=keyword)

        paper_stats_doc.set_keyword_stats(list(results.values()))
        paper_stats_doc.save(output_path)

        return paper_stats_doc.get_paper_stats()

    def is_in_ref_section(self, keyword_coordinate, reference_coordinate, page: Page, reference_page_number: int,
                          keyword_page_number: int) -> bool:
        if reference_coordinate and reference_page_number:
            keyword_col = 0 if keyword_coordinate.x0 < (page.rect.width / 2) else 1
            reference_col = 0 if reference_coordinate.x0 < (page.rect.width / 2) else 1

            is_in_reference_page = keyword_page_number == reference_page_number
            is_after_reference_page = keyword_page_number > reference_page_number
            is_coordinate_in_reference_section = keyword_coordinate.y0 >= reference_coordinate.y0 or keyword_col > reference_col

            return (is_in_reference_page and is_coordinate_in_reference_section) or is_after_reference_page
        return False

    def get_references_page_and_coordinate(self, document: Document):
        for page in reversed(document):
            lines = page.get_text(self.TEXT).splitlines()
            page_number = page.number + 1

            for line in lines:
                stripped = line.strip().lower()

                if self.REFERENCE_PATTERN.match(re.sub(r'(?<=\w)\s+(?=\w)', '', stripped)):
                    return page.search_for(line.rstrip('.-'))[0], page_number
        return None, None
