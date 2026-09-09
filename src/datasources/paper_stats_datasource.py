from collections import defaultdict
from datetime import datetime, timezone
from typing import List

from bson import ObjectId
from kink import inject

from datasources.clients.mongodb_client import MongoDBClient
from datasources.constants.field import Field
from datasources.constants.mongodb_command import MongoDBCommand
from entities.enums.phase_status import PhaseStatus
from entities.paper_stats import PaperStats


@inject
class PaperStatsDataSource:
    CONFERENCES_DB = "conferences"
    JOURNALS_DB = "journals"

    def __init__(self, mongo_client: MongoDBClient):
        self.mongo_client = mongo_client

    def save(self, paper_stats: PaperStats):
        if paper_stats.is_published_in_journal:
            database = self.mongo_client.client[self.JOURNALS_DB]
        else:
            database = self.mongo_client.client[self.CONFERENCES_DB]

        collection = database[paper_stats.venue.lower()]
        collection.insert_one(paper_stats.to_dict())

    def save_all(self, paper_stats: List[PaperStats]):
        grouped_paper_stats = defaultdict(list)

        for paper_stat in paper_stats:
            grouped_paper_stats[paper_stat.venue.lower()].append(paper_stat.to_dict())

        for venue, paper_stats_in_venue in grouped_paper_stats.items():
            if paper_stats_in_venue[0][Field.IS_PUBLISHED_IN_JOURNAL]:
                database = self.mongo_client.client[self.JOURNALS_DB]
            else:
                database = self.mongo_client.client[self.CONFERENCES_DB]

            collection = database[venue.lower()]
            collection.insert_many(paper_stats_in_venue)

    def find_accepted_papers_by_venue(self, venue: str, fields: List[str] = None, phase_1_status: PhaseStatus = None,
                                      phase_2_status: PhaseStatus = None) -> List[str]:
        search_filter = {}
        if phase_1_status:
            search_filter[Field.PHASE_1_STATUS] = phase_1_status.value
        if phase_2_status:
            search_filter[Field.PHASE_2_STATUS] = phase_2_status.value

        search_filter[Field.ID] = {
            MongoDBCommand.GTE: ObjectId.from_datetime(
                datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
            )
        }

        projection = {}

        if fields:
            projection = {field_name: 1 for field_name in fields}

        collection = self.__get_collection_by_venue(venue)

        return list(collection.find(search_filter, projection))

    def update_phase_2_paper_status(self, paper_id_list, venue, phase_status: PhaseStatus):
        collection = self.__get_collection_by_venue(venue)

        paper_object_id_list = [ObjectId(paper_id) for paper_id in paper_id_list]

        if phase_status == PhaseStatus.REJECTED:
            collection.update_many({Field.ID: {MongoDBCommand.IN: paper_object_id_list}},
                                   {MongoDBCommand.SET: {Field.PHASE_2_STATUS: phase_status.value}})
        elif phase_status == PhaseStatus.ACCEPTED:
            collection.update_many({Field.ID: {MongoDBCommand.IN: paper_object_id_list}},
                                   {MongoDBCommand.SET: {Field.PHASE_2_STATUS: phase_status.value,
                                                         Field.PHASE_3_STATUS: PhaseStatus.PENDING.value}})

    def __get_collection_by_venue(self, venue):
        if venue.lower() in self.mongo_client.client[self.CONFERENCES_DB].list_collection_names():
            return self.mongo_client.client[self.CONFERENCES_DB][venue.lower()]
        else:
            return self.mongo_client.client[self.JOURNALS_DB][venue.lower()]
