from pathlib import Path


class PaperService:

    PDF_EXTENSION = "*.pdf"

    @staticmethod
    def get_paper_list(folder_path: str, should_include_subfolders: bool):
        folder = Path(folder_path)
        if should_include_subfolders:
            return list(folder.rglob(PaperService.PDF_EXTENSION))
        else:
            return list(folder.glob(PaperService.PDF_EXTENSION))