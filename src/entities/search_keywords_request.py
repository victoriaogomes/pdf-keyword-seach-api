from typing import List

from pydantic import ConfigDict
from pydantic.alias_generators import to_camel
from pydantic.dataclasses import dataclass


@dataclass(config=ConfigDict(alias_generator=to_camel, populate_by_name=True))
class SearchKeywordsRequest:
    keywords: List[str]
    pdf_folder_path: str
    output_path: str
    include_subfolders: bool = True
    ignore_reference_section: bool = True
