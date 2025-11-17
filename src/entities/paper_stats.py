from typing import List, Optional

from pydantic import Field
from pydantic.dataclasses import dataclass

from entities.enums.phase_status import PhaseStatus
from entities.keyword_stats import KeywordStats


@dataclass
class PaperStats:
    title: str
    filename: str
    venue: str
    publication_year: int
    page_count: int
    keyword_stats: List[KeywordStats] = Field(default_factory=list)
    is_published_in_journal: bool = None
    keywords_total: int = 0
    phase_1_status: PhaseStatus = PhaseStatus.PENDING
    phase_2_status: Optional[PhaseStatus] = None

    def to_dict(self) -> dict:
        keyword_stats_dict = [keyword_stats.to_dict() for keyword_stats in self.keyword_stats]

        main_dict = {
            "title": self.title,
            "filename": self.filename,
            "venue": self.venue,
            "page_count": self.page_count,
            "publication_year": self.publication_year,
            "keyword_stats": keyword_stats_dict,
            "keywords_total": self.keywords_total,
            "is_published_in_journal": self.is_published_in_journal,
            "phase_1_status": self.phase_1_status.value
        }

        if self.phase_2_status is not None:
            main_dict["phase_2_status"] = self.phase_2_status.value

        return main_dict
