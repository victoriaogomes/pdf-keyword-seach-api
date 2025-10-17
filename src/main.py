import uvicorn
from fastapi import FastAPI

from configs.di import Di
from transportlayer.pdf_keyword_searcher_controller import PdfKeywordSearcherController

app = FastAPI()

Di.set_up()

pdf_keyword_searcher_controller = PdfKeywordSearcherController()

app.include_router(pdf_keyword_searcher_controller.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
