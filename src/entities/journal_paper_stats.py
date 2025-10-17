from typing import Optional


from entities.paper_stats import PaperStats


class JournalPaperStats(PaperStats):
    volume: int
    issue: Optional[int]
    meta = {"db_alias": "journals"}

    def __init__(self, title: str, venue: str, volume: int, publication_year: int, file_name: str, issue: int = None):
        super().__init__(title, venue, publication_year, file_name)
        self.is_published_in_journal = True
        self.volume = volume
        self.issue = issue

    def to_dict(self) -> dict:
        main_data = super().to_dict()
        main_data['volume'] = self.volume

        if self.issue is not None:
            main_data['issue'] = self.issue

        return main_data
