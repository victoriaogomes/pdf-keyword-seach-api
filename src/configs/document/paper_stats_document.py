import re
from collections import defaultdict
from pathlib import Path

from pymupdf import pymupdf, Document

from entities.conference_paper_stats import ConferencePaperStats
from entities.enums.phase_status import PhaseStatus
from entities.journal_paper_stats import JournalPaperStats
from utils.constants import CONFERENCES, JOURNALS


class PaperStatsDocument:
    BOOKMARK_1ST_LEVEL = 1
    BOOKMARK_2ND_LEVEL = 2
    KEYWORD_OCCURRENCE_HIGHLIGHT_COMMENT = "Occurrence {} of {}"
    KEYWORD_OCCURRENCE_1ST_LEVEL = "{} occurrences ({})"
    KEYWORD_OCCURRENCE_2ND_LEVEL = "{} occurrence {}"
    JOURNAL_FOLDER_PATTERN = r"Volume (\d+)(?: - Issue (\d+))?"
    LOG_ERROR_PROCESSING_PAPER = "Error processing paper {}"

    def __init__(self, path: Path):
        self.doc = pymupdf.open(path)
        self.path = path
        self.paper_stats = self.__get_paper_stats_object()
        self.toc = []
        self.bookmark_counter = defaultdict(int)
        self.parent_bookmarks = {}

    def add_toc_entry(self, keyword, page_number):
        if keyword not in self.parent_bookmarks:
            self.parent_bookmarks[keyword] = len(self.toc)
            self.toc.append(self.__get_toc_entry_occurrence_by_level(self.BOOKMARK_1ST_LEVEL, keyword, page_number))
        self.bookmark_counter[keyword] += 1
        parent_index = self.parent_bookmarks[keyword]
        self.toc[parent_index][1] = self.KEYWORD_OCCURRENCE_1ST_LEVEL.format(keyword, self.bookmark_counter[keyword])
        self.toc.append(self.__get_toc_entry_occurrence_by_level(self.BOOKMARK_2ND_LEVEL, keyword, page_number))

    def __get_toc_entry_occurrence_by_level(self, level, keyword, page_number):
        if level == self.BOOKMARK_1ST_LEVEL:
            occurrence_text = self.KEYWORD_OCCURRENCE_1ST_LEVEL.format(keyword, self.bookmark_counter[keyword])
        else:
            occurrence_text = self.KEYWORD_OCCURRENCE_2ND_LEVEL.format(keyword, self.bookmark_counter[keyword])
        return [level, occurrence_text, page_number]

    def get_doc(self):
        return self.doc

    def get_paper_stats(self):
        return self.paper_stats

    def save(self, output_path: str):
        if self.toc:
            self.doc.set_toc(self.toc, collapse=2)

            self.__update_paper_stats_phase()

            base_output_path = Path(output_path)

            processed_pdf_path = base_output_path / self.get_relative_subpath()
            processed_pdf_path.parent.mkdir(parents=True, exist_ok=True)

            self.doc.save(processed_pdf_path, garbage=4, deflate=True)
        self.doc.close()

    def get_relative_subpath(self) -> Path:
        for key in ("Conferences", "Journals"):
            if key in self.path.parts:
                return Path(*self.path.parts[self.path.parts.index(key):])
        raise ValueError("Neither 'Conferences' nor 'Journals' found in path")

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
        file_name = parts[-1]
        title = self.get_paper_title(self.doc)

        try:
            idx = next(i for i, p in enumerate(lower_parts) if p in (CONFERENCES, JOURNALS))
            publication_type = parts[idx]
            venue = parts[idx + 1] if len(parts) > idx + 1 else None
            year = parts[idx + 2] if len(parts) > idx + 2 else None

            if publication_type.lower() == CONFERENCES.lower():
                track = parts[idx + 3] if len(parts) > idx + 3 else None
                return ConferencePaperStats(title=title, venue=venue, track=track,
                                            publication_year=int(year), file_name=file_name)
            else:
                match = re.match(self.JOURNAL_FOLDER_PATTERN, parts[idx + 3] if len(parts) > idx + 3 else None)

                return JournalPaperStats(title=title, venue=venue, volume=int(match.group(1)),
                                         publication_year=int(year), file_name=file_name,
                                         issue=int(match.group(2)) if match.group(2) else None)
        except StopIteration:
            print(self.LOG_ERROR_PROCESSING_PAPER.format(lower_parts[-1]))

    def highlight_keyword(self, page, instance, keyword):
        annot = page.add_highlight_annot(instance)
        annot.set_colors(stroke=pymupdf.pdfcolor["pink"])
        annot.set_info(content=self.KEYWORD_OCCURRENCE_HIGHLIGHT_COMMENT.format(self.bookmark_counter[keyword],
                                                                                keyword))
        annot.update()

    def get_paper_title(self, doc: Document):
        blocks = doc[0].get_text("dict")["blocks"]
        spans = []
        for b in blocks:
            for line in b.get("lines", []):
                for span in line.get("spans", []):
                    text = span["text"].strip()
                    if len(text) > 2:
                        spans.append((span["size"], span["bbox"][1], text))

        if not spans:
            return ""

        spans.sort(key=lambda x: (-x[0], x[1]))
        max_font_size = spans[0][0]

        title_lines = []
        for size, y, text in spans:
            if abs(size - max_font_size) < 1e-2:
                title_lines.append(text)
            else:
                break

        return " ".join(title_lines).strip()
