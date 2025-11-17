import json
from pathlib import Path
from typing import List

from entities.paper_stats import PaperStats


class JsonConverter:

    @staticmethod
    def to_json(papers: List[PaperStats], output_path: str):
        path = Path(output_path) / "processed_papers.json"
        json_result = []

        for paper in papers:
            json_result.append(paper.to_dict())

        with path.open("w", encoding="utf-8") as f:
            json.dump(json_result, f, ensure_ascii=False, indent=2)

        print("File saved!")
