class KeywordStats:
    def __init__(self, keyword: str):
        self.keyword: str = keyword
        self.total = 0
        self.by_page = {}

    def add_occurrence(self, page_number: int, count: int = 1):
        self.total += count
        self.by_page[page_number] = self.by_page.get(page_number, 0) + count

    def to_dict(self):
        return {
            "keyword": self.keyword,
            "total": self.total,
            "by_page": [
                {"page": page, "count": count} for page, count in self.by_page.items()
            ]
        }
