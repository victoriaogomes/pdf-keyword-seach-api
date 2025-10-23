from typing import List

from kink import inject

from datasources.clients.open_search_client import OpenSearchClient
from datasources.constants.field import Field
from entities.enums.phase_status import PhaseStatus


@inject
class OpenSearchDatasource:
    INDEX_NAME = 'papers'

    def __init__(self, open_search_client: OpenSearchClient):
        self.open_search_client = open_search_client

    def update_records(self, id_list: List[str], phase_status: PhaseStatus):
        action_list = []

        for paper_id in id_list:
            action_list.append({'update': {'_index': self.INDEX_NAME, Field.ID: paper_id}})
            if phase_status == PhaseStatus.ACCEPTED:
                action_list.append(
                    {'doc': {Field.PHASE_2_STATUS: phase_status.value,
                             Field.PHASE_3_STATUS: PhaseStatus.PENDING.value}})
            elif phase_status == PhaseStatus.REJECTED:
                action_list.append({'doc': {Field.PHASE_2_STATUS: phase_status.value}})

        try:
            response = self.open_search_client.client.bulk(body=action_list)

            # 4. Check the response for errors
            if response['errors']:
                print("\n⚠️ Bulk update completed with ERRORS:")
                for item in response['items']:
                    if item['update']['status'] >= 400:
                        print(
                            f"  ID: {item['update']['_id']}, Status: {item['update']['status']}, Error: {item['update']['error']['type']}")
            else:
                print("\n✅ Bulk update successful!")
                print(f"Total actions processed: {len(response['items'])}")

        except Exception as e:
            print(f"\n❌ An error occurred during the request: {e}")
