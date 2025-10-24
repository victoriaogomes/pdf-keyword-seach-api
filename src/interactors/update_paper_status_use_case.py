import pandas as pd
from kink import inject

from datasources.open_search_datasource import OpenSearchDatasource
from datasources.paper_stats_datasource import PaperStatsDataSource
from entities.enums.phase_status import PhaseStatus


@inject
class UpdatePaperStatusUseCase:

    def __init__(self, paper_stats_datasource: PaperStatsDataSource, open_search_datasource: OpenSearchDatasource):
        self.open_search_datasource = open_search_datasource
        self.paper_stats_datasource = paper_stats_datasource

    def execute(self, file_path: str, venue):
        try:
            accepted_papers = []
            rejected_papers = []
            df = pd.read_excel(file_path)

            for index, row in df.iterrows():
                status = row['Paper evaluation status'].lower()
                if status == PhaseStatus.REJECTED.value:
                    rejected_papers.append(row['Id'])
                elif status == PhaseStatus.ACCEPTED.value:
                    accepted_papers.append(row['Id'])

            self.paper_stats_datasource.update_phase_2_paper_status(accepted_papers, venue, PhaseStatus.ACCEPTED)
            self.open_search_datasource.update_records(accepted_papers, PhaseStatus.ACCEPTED)
            self.paper_stats_datasource.update_phase_2_paper_status(rejected_papers, venue, PhaseStatus.REJECTED)
            self.open_search_datasource.update_records(rejected_papers, PhaseStatus.REJECTED)
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
