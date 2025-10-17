import re
from collections import Counter
from pathlib import Path
from typing import List

from kink import inject

from datasources.paper_stats_datasource import PaperStatsDataSource
from entities.keyword_stats import KeywordStats
from configs.document.paper_stats_document import PaperStatsDocument


@inject
class PdfKeywordSearcher:
    PDF_EXTENSION = "*.pdf"
    REFERENCE_KEYWORDS = ["references", "bibliography", "works cited"]

    LOG_AMOUNT_OF_PAPERS_TO_PROCESS = "There are {} papers to process in the chosen folder."
    LOG_STEP_UPDATE = "Finished processing paper {}/{}: {}"

    PIPE = "|"
    TEXT = "text"

    def __init__(self, paper_stats_datasource: PaperStatsDataSource):
        self.paper_stats_datasource = paper_stats_datasource

    def analyze_papers_in_path(self, path: str, keywords: List[str], should_include_subfolders: bool,
                               should_ignore_reference_section: bool, output_path: str):
        results = []
        papers_to_process = self.__get_paper_list(path, should_include_subfolders)
        print(self.LOG_AMOUNT_OF_PAPERS_TO_PROCESS.format(len(papers_to_process)))
        keyword_patterns = [re.escape(k.lower()) for k in keywords]
        keyword_patterns.sort(key=len, reverse=True)
        keyword_regex_pattern = re.compile(r'\b(?:' + self.PIPE.join(keyword_patterns) + r')\b', re.IGNORECASE)

        for index, pdf_file in enumerate(papers_to_process):
            results.append(self.__search_for_keywords_in_paper(pdf_file, keywords, keyword_regex_pattern,
                                                               should_ignore_reference_section, output_path))
            print(self.LOG_STEP_UPDATE.format(index + 1, len(papers_to_process), pdf_file))

        # self.paper_stats_datasource.save_all(results)
        return results

    def __get_paper_list(self, folder_path: str, should_include_subfolders: bool):
        folder = Path(folder_path)
        if should_include_subfolders:
            return list(folder.rglob(self.PDF_EXTENSION))
        else:
            return list(folder.glob(self.PDF_EXTENSION))

    def __search_for_keywords_in_paper(self, pdf_file: Path, keywords: List[str], keyword_regex_pattern: re,
                                       should_ignore_reference_section: bool, output_path: str):
        paper_stats_doc: PaperStatsDocument = PaperStatsDocument(pdf_file)

        found_references = False

        results = {kw: KeywordStats(kw) for kw in keywords}

        for page in paper_stats_doc.get_doc():
            lines = page.get_text(self.TEXT).splitlines()
            page_number = page.number + 1

            for line in lines:
                stripped = line.strip().lower()

                if should_ignore_reference_section and any(stripped == kw for kw in self.REFERENCE_KEYWORDS):
                    found_references = True
                    break

                keyword_matches = keyword_regex_pattern.findall(stripped)

                if keyword_matches:
                    match_counts = Counter(keyword_matches)

                    for keyword_match, count in match_counts.items():
                        original_keyword = next((kw for kw in keywords if kw.lower() == keyword_match), None)

                        if original_keyword:
                            results[original_keyword].add_occurrence(page_number, count)

                            paper_stats_doc.increase_keyword_total_count(count)

                            line_rect = page.search_for(stripped)[0]

                            keyword_instances = page.search_for(original_keyword, clip=line_rect)
                            for inst in keyword_instances:
                                paper_stats_doc.add_toc_entry(original_keyword, page_number)

                                paper_stats_doc.highlight_keyword(page=page, instance=inst,
                                                                  keyword=original_keyword)

            if found_references:
                break

        paper_stats_doc.set_keyword_stats(list(results.values()))
        paper_stats_doc.save(output_path)

        return paper_stats_doc.get_paper_stats()
