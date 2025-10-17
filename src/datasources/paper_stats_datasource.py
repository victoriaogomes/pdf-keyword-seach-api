from collections import defaultdict
from typing import List

from kink import inject

from configs.db.mongodb_client import MongoDBClient
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

        # papers_sorted = sorted(paper_stats, key=lambda x: x.venue)

        # paper_stats_grouped_by_venue = {k: list(v) for k, v in groupby(papers_sorted, key=lambda x: x.venue)}

        for paper_stat in paper_stats:
            grouped_paper_stats[paper_stat.venue.lower()].append(paper_stat.to_dict())

        for venue, paper_stats_in_venue in grouped_paper_stats.items():
            if paper_stats_in_venue[0]["is_published_in_journal"]:
                database = self.mongo_client.client[self.JOURNALS_DB]
            else:
                database = self.mongo_client.client[self.CONFERENCES_DB]

            collection = database[venue.lower()]
            collection.insert_many(paper_stats_in_venue)
