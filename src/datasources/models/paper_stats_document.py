import itertools
from pathlib import Path
from typing import List

from pymupdf import pymupdf

from datasources.models.toc_entry import TocEntry
from entities.paper_stats import PaperStats
from utils.constants import BOOKMARK_1ST_LEVEL, BOOKMARK_2ND_LEVEL


class PaperStatsDocument:
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
        if self.toc:
            toc_list = list(itertools.chain.from_iterable([toc.to_array() for toc in self.toc]))
            self.doc.set_toc(toc_list, collapse=2)

            base_output_path = Path(output_path)

            processed_pdf_path = base_output_path / Path(self.path.stem + ".pdf")

            processed_pdf_path.parent.mkdir(parents=True, exist_ok=True)

            self.doc.save(processed_pdf_path, garbage=4, deflate=True)
        self.doc.close()

    def increase_keyword_total_count(self, count):
        self.paper_stats.keywords_total += count

    def set_keyword_stats(self, keyword_stats):
        self.paper_stats.keyword_stats = keyword_stats

    def __get_paper_stats_object(self) -> PaperStats:
        parts = self.path.parts
        filename = parts[self.LAST_ARRAY_INDEX]
        title = self.get_paper_title(filename)
        page_count = self.doc.page_count

        return PaperStats(title=title, filename=filename, page_count=page_count)

    def highlight_keyword(self, page, instance, keyword):
        parent_index = self.parent_bookmarks[keyword]
        parent = self.toc[parent_index]

        annot = page.add_highlight_annot(instance)

        annot.set_colors(stroke=pymupdf.pdfcolor[self.PINK_COLOR])
        annot.set_info(content=self.KEYWORD_OCCURRENCE_HIGHLIGHT_COMMENT.format(parent.counter, keyword))
        annot.update()

    def get_paper_title(self, filename: str):
        return self.doc.metadata[self.TITLE] if self.doc.metadata[self.TITLE] else filename
