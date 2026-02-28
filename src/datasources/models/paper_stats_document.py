import itertools
import re
from pathlib import Path
from typing import List

from pymupdf import pymupdf

from datasources.models.toc_entry import TocEntry
from entities.conference_paper_stats import ConferencePaperStats
from entities.enums.phase_status import PhaseStatus
from entities.journal_paper_stats import JournalPaperStats
from utils.constants import CONFERENCES, JOURNALS, BOOKMARK_1ST_LEVEL, BOOKMARK_2ND_LEVEL


class PaperStatsDocument:
    JOURNAL_FOLDER_PATTERN = r"Volume (\d+)(?: - Issue (\d+))?"
    KEYWORD_OCCURRENCE_HIGHLIGHT_COMMENT = "Occurrence {} of {}"
    LAST_ARRAY_INDEX = -1
    LOG_ERROR_PROCESSING_PAPER = "Error processing paper {}"
    PINK_COLOR = "pink"
    TITLE = "title"
    SLASH = "/"

    def __init__(self, path: Path):
        self.doc = pymupdf.open(path)
        self.path = path
        self.paper_stats = self.__get_paper_stats_object()
        self.toc: List[TocEntry] = []
        self.parent_bookmarks = {}

    def add_toc_entry(self, keyword, page_number):
        if keyword not in self.parent_bookmarks:
            self.parent_bookmarks[keyword] = len(self.toc)
            self.toc.append(TocEntry(page_number=page_number, level=BOOKMARK_1ST_LEVEL, keyword=keyword))

        parent_index = self.parent_bookmarks[keyword]
        parent = self.toc[parent_index]
        parent.add_child(TocEntry(page_number=page_number, level=BOOKMARK_2ND_LEVEL, keyword=keyword,
                                  counter=parent.counter + 1))

    def get_doc(self):
        return self.doc

    def get_paper_stats(self):
        return self.paper_stats

    def save(self, output_path: str):
        self.__update_paper_stats_phase()

        if self.toc:
            toc_list = list(itertools.chain.from_iterable([toc.to_array() for toc in self.toc]))
            self.doc.set_toc(toc_list, collapse=2)

            base_output_path = Path(output_path)
            main_folder = JOURNALS.capitalize() if self.paper_stats.is_published_in_journal else CONFERENCES.capitalize()

            processed_pdf_path = base_output_path / Path(
                main_folder + self.SLASH + self.paper_stats.venue.upper() + self.SLASH + self.path.stem + ".pdf")
            processed_pdf_path.parent.mkdir(parents=True, exist_ok=True)

            self.doc.save(processed_pdf_path, garbage=4, deflate=True)
        self.doc.close()

    def increase_keyword_total_count(self, count):
        self.paper_stats.keywords_total += count

    def set_keyword_stats(self, keyword_stats):
        self.paper_stats.keyword_stats = keyword_stats

    def __update_paper_stats_phase(self):
        if self.paper_stats.keywords_total > 0:
            self.paper_stats.phase_1_status = PhaseStatus.ACCEPTED
            self.paper_stats.phase_2_status = PhaseStatus.PENDING
        else:
            self.paper_stats.phase_1_status = PhaseStatus.REJECTED

    def __get_paper_stats_object(self):
        parts = self.path.parts
        lower_parts = [p.lower() for p in parts]
        filename = parts[self.LAST_ARRAY_INDEX]
        title = self.get_paper_title(filename)

        try:
            idx = next(i for i, p in enumerate(lower_parts) if p in (CONFERENCES, JOURNALS))
            publication_type = parts[idx] if idx else None
            venue = parts[idx + 1] if idx and len(parts) > idx + 1 else None
            year = parts[idx + 2] if idx and len(parts) > idx + 2 else None

            if publication_type.lower() == CONFERENCES.lower():
                track = parts[idx + 3] if len(parts) > idx + 3 else None
                return ConferencePaperStats(title=title, venue="", track="", page_count=self.doc.page_count,
                                            publication_year=0, filename=filename)
            else:
                match = re.match(self.JOURNAL_FOLDER_PATTERN, parts[idx + 3] if len(parts) > idx + 3 else None)
                volume = int(match.group(1)) if match.group(1) else 0
                issue = int(match.group(2)) if match.group(2) else 0

                return JournalPaperStats(title=title, venue="", volume=0, publication_year=0,
                                         filename=filename, page_count=self.doc.page_count, issue=0)
        except StopIteration:
            print(self.LOG_ERROR_PROCESSING_PAPER.format(lower_parts[self.LAST_ARRAY_INDEX]))

    def highlight_keyword(self, page, instance, keyword):
        parent_index = self.parent_bookmarks[keyword]
        parent = self.toc[parent_index]

        annot = page.add_highlight_annot(instance)

        annot.set_colors(stroke=pymupdf.pdfcolor[self.PINK_COLOR])
        annot.set_info(content=self.KEYWORD_OCCURRENCE_HIGHLIGHT_COMMENT.format(parent.counter, keyword))
        annot.update()

    def get_paper_title(self, filename: str):
        return self.doc.metadata[self.TITLE] if self.doc.metadata[self.TITLE] else filename
