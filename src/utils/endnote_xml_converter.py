import xml.etree.ElementTree as ET


class EndnoteXmlConverter:
    @staticmethod
    def to_endnote_xml(records, output_file="endnote.xml"):
        # Root structure required by EndNote
        root = ET.Element("xml")
        records_el = ET.SubElement(root, "records")

        for rec in records:
            record_el = ET.SubElement(records_el, "record")

            # Reference type 17 = Conference Paper (EndNote mapping)
            ref_type = ET.SubElement(record_el, "ref-type", {"name": "Conference Paper"})
            ref_type.text = "17"

            # -------------------
            # Authors
            # -------------------
            contributors_el = ET.SubElement(record_el, "contributors")
            authors_el = ET.SubElement(contributors_el, "authors")
            for author in rec["Authors"]:
                author_el = ET.SubElement(authors_el, "author")
                author_el.text = author

            # -------------------
            # Titles
            # -------------------
            titles_el = ET.SubElement(record_el, "titles")
            title_el = ET.SubElement(titles_el, "title")
            title_el.text = rec["Title"]

            # -------------------
            # Year
            # -------------------
            dates_el = ET.SubElement(record_el, "dates")
            year_el = ET.SubElement(dates_el, "year")
            year_el.text = rec["Publication Year"]

            # -------------------
            # DOI
            # -------------------
            if rec.get("DOI"):
                doi_el = ET.SubElement(record_el, "electronic-resource-num")
                doi_el.text = rec["DOI"]

            # -------------------
            # Venue (Conference name)
            # -------------------
            if rec.get("Venue"):
                periodical_el = ET.SubElement(record_el, "periodical", {"full-title": rec["Venue"]})

            # -------------------
            # Abstract (NEW)
            # -------------------
            if rec.get("Abstract"):
                abstract_el = ET.SubElement(record_el, "abstract")
                style_el = ET.SubElement(abstract_el, "style", {"face": "normal", "font": "default"})
                style_el.text = rec["Abstract"]

        # Write output XML
        tree = ET.ElementTree(root)
        tree.write(output_file, encoding="utf-8", xml_declaration=True)

        return output_file
