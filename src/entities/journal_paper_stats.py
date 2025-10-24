from typing import Optional

from pydantic.dataclasses import dataclass

from entities.paper_stats import PaperStats
from utils.constants import VOLUME, ISSUE

@dataclass
class JournalPaperStats(PaperStats):
    volume: int = None
    issue: Optional[int] = None
    is_published_in_journal: bool = True

    def to_dict(self) -> dict:
        main_data = super().to_dict()
        main_data[VOLUME] = self.volume

        if self.issue is not None:
            main_data[ISSUE] = self.issue

        return main_data
