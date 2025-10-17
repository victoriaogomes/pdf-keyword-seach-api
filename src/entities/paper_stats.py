from typing import List

from entities.enums.phase_status import PhaseStatus
from entities.keyword_stats import KeywordStats


class PaperStats:
    title: str
    file_name: str
    venue: str
    publication_year: int
    keyword_stats: List[KeywordStats]
    is_published_in_journal: bool
    keywords_total: int = 0
    phase_1_status: PhaseStatus = PhaseStatus.PENDING
    phase_2_status: PhaseStatus = None

    def __init__(self, title: str, venue: str, publication_year: int, file_name: str):
        self.title = title
        self.venue = venue
        self.publication_year = publication_year
        self.file_name = file_name

    def to_dict(self) -> dict:
        # keywords = [keyword_stat.keyword for keyword_stat in self.keyword_stats if keyword_stat.total > 0]
        # keywords_total = sum(keyword_stat.total for keyword_stat in self.keyword_stats)
        keyword_stats_dict = [keyword_stats.to_dict() for keyword_stats in self.keyword_stats]
        main_dict = {
            "title": self.title,
            "filename": self.file_name,
            "venue": self.venue,
            "publication_year": self.publication_year,
            "keyword_stats": keyword_stats_dict,
            "keywords_total": self.keywords_total,
            "is_published_in_journal": self.is_published_in_journal,
            "phase_1_status": self.phase_1_status.value
        }

        if self.phase_2_status is not None:
            main_dict["phase_2_status"] = self.phase_2_status.value

        return main_dict
