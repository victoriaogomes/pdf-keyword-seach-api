from kink import inject

from datasources.paper_metadata_datasource import PaperDatasource
from entities.enums.paper_metadata import PaperMetadata
from utils.endnote_xml_converter import EndnoteXmlConverter


@inject
class GetPaperMetadataUseCase:

    COMMA = ","

    def __init__(self, paper_datasource: PaperDatasource):
        self.paper_datasource = paper_datasource

    def execute(self, folder_path: str, should_include_subfolders: bool = True, fields: str = None):
        metadata_fields = self.__load_metadata_fields(fields)

        paper_list = self.paper_datasource.get_paper_metadata(folder_path, should_include_subfolders,
                                                              metadata_fields)
        print(paper_list)
        EndnoteXmlConverter.to_endnote_xml(paper_list)

    def __load_metadata_fields(self, fields: str = None):
        if not fields:
            return [e for e in PaperMetadata]
        else:
            field_list = fields.split(self.COMMA)
            return [PaperMetadata.from_string(field) for field in field_list]
