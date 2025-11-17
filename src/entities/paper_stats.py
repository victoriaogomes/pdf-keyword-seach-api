from typing import List

from pydantic import Field
from pydantic.dataclasses import dataclass

from entities.keyword_stats import KeywordStats


@dataclass
class PaperStats:
    title: str
    filename: str
    page_count: int
    keyword_stats: List[KeywordStats] = Field(default_factory=list)
    keywords_total: int = 0

    def to_dict(self) -> dict:
        keyword_stats_dict = [keyword_stats.to_dict() for keyword_stats in self.keyword_stats if
                              keyword_stats.total > 0]

        main_dict = {
            "title": self.title,
            "filename": self.filename,
            "page_count": self.page_count,
            "keywords_total": self.keywords_total,
            "keyword_stats": keyword_stats_dict
        }

        return main_dict
