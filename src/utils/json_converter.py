import json
from typing import List

from entities.paper_stats import PaperStats


class JsonConverter:

    @staticmethod
    def pdf_stats_list_to_json(pdf_stats_list: List[PaperStats]):
        json_result = []

        for pdf_stats in pdf_stats_list:
            json_result.append(pdf_stats.to_dict())

        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(json_result, f, ensure_ascii=False, indent=2)

    @staticmethod
    def pdf_stats_list_to_ndjson(pdf_stats_list: List[PaperStats]):
        json_result = []

        for pdf_stats in pdf_stats_list:
            json_result.append(pdf_stats.to_dict())

        with open("data.ndjson", "w", encoding="utf-8") as f:
            for doc in json_result:
                f.write(json.dumps({"index": {"_index": "papers"}}, ensure_ascii=False) + "\n")
                f.write(json.dumps(doc, ensure_ascii=False) + "\n")
