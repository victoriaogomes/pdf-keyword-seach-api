from entities.paper_stats import PaperStats
from utils.constants import TRACK


class ConferencePaperStats(PaperStats):
    track: str

    def __init__(self, title: str, venue: str, track: str, publication_year: int, filename: str):
        super().__init__(title, venue, publication_year, filename)
        self.is_published_in_journal = False
        self.track = track

    def to_dict(self) -> dict:
        main_data = super().to_dict()
        main_data[TRACK] = self.track

        return main_data
