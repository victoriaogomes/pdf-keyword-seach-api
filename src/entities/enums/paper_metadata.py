from enum import Enum


class PaperMetadata(Enum):
    TITLE = "Title"
    ABSTRACT = "Abstract"
    DOI = "DOI"
    PAGE_COUNT = "Page count"
    AUTHORS = "Authors"
    VENUE = "Venue"
    PUBLICATION_YEAR = "Publication Year"

    @classmethod
    def from_string(cls, field) -> "PaperMetadata":
        lookup = {m.value.lower(): m for m in cls}

        if field not in lookup:
            raise ValueError(f"Unknown metadata field: {field}")

        return lookup[field]
