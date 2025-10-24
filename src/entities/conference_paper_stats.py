from pydantic.dataclasses import dataclass

from entities.paper_stats import PaperStats
from utils.constants import TRACK


@dataclass
class ConferencePaperStats(PaperStats):
    track: str = None
    is_published_in_journal: bool = False

    def to_dict(self) -> dict:
        main_data = super().to_dict()
        main_data[TRACK] = self.track

        return main_data
