from entities.paper_stats import PaperStats


class ConferencePaperStats(PaperStats):
    track: str

    def __init__(self, title: str, venue: str, track: str, publication_year: int, file_name: str):
        super().__init__(title, venue, publication_year, file_name)
        self.is_published_in_journal = False
        self.track = track

    def to_dict(self) -> dict:
        main_data = super().to_dict()
        main_data['track'] = self.track

        return main_data
