from typing import List

from entities.camel_base_model import CamelBaseModel


class SearchKeywordsRequest(CamelBaseModel):
    keywords: List[str]
    pdf_folder_path: str
    output_path: str
    should_include_subfolders: bool = True
    should_ignore_reference_section: bool = True
