from dotmap import DotMap
from kink import inject

from datasources.paper_stats_datasource import PaperStatsDataSource
from entities.enums.output_format import OutputFormat
from utils.json_converter import JsonConverter
from utils.xlsx_converter import XlsxConverter


@inject
class GetPapersByVenueUseCase:
    COMMA = ","

    def __init__(self, paper_stats_datasource: PaperStatsDataSource):
        self.paper_stats_datasource = paper_stats_datasource

    def execute(self, venue: str, output_format: OutputFormat, fields: str = None, phase_1_status: str = None,
                phase_2_status: str = None) -> None:
        field_list = fields.split(self.COMMA) if fields else None
        paper_list = self.paper_stats_datasource.find_accepted_papers_by_venue(venue, field_list, phase_1_status,
                                                                               phase_2_status)

        paper_list_dot_map = [DotMap(paper) for paper in paper_list]

        if output_format == OutputFormat.XLSX:
            XlsxConverter.to_xlsx(paper_list_dot_map, venue, field_list)
        else:
            JsonConverter.paper_list_to_json(paper_list, venue)
            JsonConverter.pdf_stats_list_to_ndjson(paper_list, venue)
