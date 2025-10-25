from typing import List

from pydantic import Field
from pydantic.dataclasses import dataclass

from utils.constants import BOOKMARK_1ST_LEVEL


@dataclass
class TocEntry:
    KEYWORD_OCCURRENCE_1ST_LEVEL = "{} occurrences ({})"
    KEYWORD_OCCURRENCE_2ND_LEVEL = "{} occurrence {}"

    page_number: int
    level: int
    keyword: str
    title: str = None
    counter: int = 0
    children: List['TocEntry'] = Field(default_factory=list)

    def __post_init__(self):
        self.__update_title()

    def add_child(self, child: 'TocEntry'):
        self.children.append(child)
        self.counter += 1
        self.__update_title()

    def __update_title(self):
        if self.level == BOOKMARK_1ST_LEVEL:
            self.title = self.KEYWORD_OCCURRENCE_1ST_LEVEL.format(self.keyword, self.counter)
        else:
            self.title = self.KEYWORD_OCCURRENCE_2ND_LEVEL.format(self.keyword, self.counter)


    def to_array(self) -> List[List[str]]:
        return [
            [self.level, self.title, self.page_number],
            *[[toc.level, toc.title, toc.page_number] for toc in self.children]
        ]