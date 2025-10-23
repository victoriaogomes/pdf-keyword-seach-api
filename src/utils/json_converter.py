import json


class JsonConverter:

    @staticmethod
    def paper_list_to_json(paper_list, venue):
        json_result = []

        for paper in paper_list:
            paper["_id"] = str(paper["_id"])
            json_result.append(paper)

        with open(f"papers-{venue}.json", "w", encoding="utf-8") as f:
            json.dump(json_result, f, ensure_ascii=False, indent=2)

    @staticmethod
    def pdf_stats_list_to_ndjson(paper_list, venue):
        json_result = []

        for paper in paper_list:
            paper["_id"] = str(paper["_id"])
            json_result.append(paper)

        with open(f"papers-{venue}.ndjson", "w", encoding="utf-8") as f:
            for doc in json_result:
                f.write(json.dumps({"index": {"_index": "papers", "_id": doc["_id"]}}, ensure_ascii=False) + "\n")
                del doc["_id"]
                f.write(json.dumps(doc, ensure_ascii=False) + "\n")
