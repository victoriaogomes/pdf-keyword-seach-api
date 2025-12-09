import requests
import xml.etree.ElementTree as ET

from datasources.models.paper_raw_metadata import PaperRawMetadata


class GrobidClient:

    @staticmethod
    def get_paper_metadata(paper):
        with open(paper, "rb") as f:
            r = requests.post(
                "http://localhost:8070/api/processHeaderDocument",
                files={"input": f},
                data={"consolidateHeader": 1},
                headers={"Accept": "application/xml"}
            )

        return PaperRawMetadata(ET.ElementTree(ET.fromstring(r.text)))
