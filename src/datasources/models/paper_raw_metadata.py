from typing import Union, List
from xml.etree.ElementTree import ElementTree


class PaperRawMetadata:
    NS = {"tei": "http://www.tei-c.org/ns/1.0"}
    TITLE_TAG = ".//tei:analytic/tei:title"
    ABSTRACT_TAG = ".//tei:abstract/tei:p"
    AUTHOR_TAG = ".//tei:analytic/tei:author"
    DOI_TAG = ".//tei:biblStruct/tei:idno[@type='DOI']"
    VENUE_TAG = ".//tei:biblStruct/tei:monogr/tei:title"
    DATE_TAG = ".//tei:biblStruct/tei:monogr/tei:imprint/tei:date[@type='published']"
    PERS_NAME = "tei:persName"
    FORENAME = "tei:forename"
    SURNAME = "tei:surname"
    WHEN = "when"
    HYPHEN = "-"

    def __init__(self, raw_data: ElementTree):
        self.raw_data = raw_data.getroot()

    def get_title(self) -> Union[str, None]:
        title_elem = self.raw_data.find(self.TITLE_TAG, self.NS)
        if title_elem is not None and title_elem.text:
            return title_elem.text.strip()
        return None

    def get_abstract(self):
        abstract_elem = self.raw_data.find(self.ABSTRACT_TAG, self.NS)

        if abstract_elem is not None:
            return abstract_elem.text.strip()
        return None

    def get_authors(self) -> List[str]:
        authors = []
        for author in self.raw_data.findall(self.AUTHOR_TAG, self.NS):
            pers = author.find(self.PERS_NAME, self.NS)
            if pers is None:
                continue
            first_names = [fn.text for fn in pers.findall(self.FORENAME, self.NS) if fn.text]
            last_names = [ln.text for ln in pers.findall(self.SURNAME, self.NS) if ln.text]
            if first_names and last_names:
                full_name = " ".join(first_names + last_names)
                authors.append(full_name)

        return authors

    def get_doi(self) -> Union[str, None]:
        doi_elem = self.raw_data.find(self.DOI_TAG, self.NS)
        if doi_elem is not None and doi_elem.text:
            return doi_elem.text.strip()
        return None

    def get_venue(self) -> Union[str, None]:
        venue_elem = self.raw_data.find(self.VENUE_TAG, self.NS)
        if venue_elem is not None and venue_elem.text:
            return venue_elem.text.strip()
        return None

    def get_publication_year(self) -> Union[str, None]:
        date_elem = self.raw_data.find(self.DATE_TAG, self.NS)
        if date_elem is not None:
            year = date_elem.get(self.WHEN)
            if year:
                return year.split(self.HYPHEN)[0]
        return None
