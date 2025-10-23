from typing import Optional

from entities.paper_stats import PaperStats
from utils.constants import VOLUME, ISSUE


class JournalPaperStats(PaperStats):
    volume: int
    issue: Optional[int]

    def __init__(self, title: str, venue: str, volume: int, publication_year: int, filename: str, issue: int = None):
        super().__init__(title, venue, publication_year, filename)
        self.is_published_in_journal = True
        self.volume = volume
        self.issue = issue

    def to_dict(self) -> dict:
        main_data = super().to_dict()
        main_data[VOLUME] = self.volume

        if self.issue is not None:
            main_data[ISSUE] = self.issue

        return main_data
