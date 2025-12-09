import uvicorn
from fastapi import FastAPI

from configs.di import Di
from transportlayer.paper_controller import PaperController

app = FastAPI()

Di.set_up()

pdf_keyword_searcher_controller = PaperController()

app.include_router(pdf_keyword_searcher_controller.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
