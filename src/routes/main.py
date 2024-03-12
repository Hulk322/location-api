""" import modules """
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.utility.spacy_prediction import SpacyPrediction
from src.config.config import settings
from .location import location_router
from .location_extractor import location_extractor_route

app = FastAPI()
@app.on_event("startup")
async def startup_event():
    SpacyPrediction()

origins = settings.default.allowed_hosts
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    location_router,
    prefix="/v1/location"
)

app.include_router(
    location_extractor_route,
    tags=["location extration"],
)


def main():
    """ main function """
    uvicorn.run("src.routes.main:app", host=settings.default.host, port=settings.default.port,
                reload=True, log_level="info")


if __name__ == "__main__":
    main()
