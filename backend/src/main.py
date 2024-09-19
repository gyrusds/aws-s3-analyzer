import json
import logging
from dotenv import load_dotenv

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

import uvicorn

OUTPUT_FOLDER = "output"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
def get_summary():

    try:
        with open(f"{OUTPUT_FOLDER}/summary.json") as f:
            return json.load(f)
    except FileNotFoundError as ex:
        logging.error(ex)
        return ORJSONResponse(content={"error": "There is no summary"}, status_code=status.HTTP_404_NOT_FOUND)


@app.get("/{bucket_name}")
def get_bucket(bucket_name: str):

    try:
        with open(f"{OUTPUT_FOLDER}/{bucket_name}.json") as f:
            return json.load(f)
    except FileNotFoundError as ex:
        logging.error(ex)
        return ORJSONResponse(content={"error": f"There is no data for bucket {bucket_name}"}, status_code=status.HTTP_404_NOT_FOUND)


if __name__ == '__main__':
    load_dotenv()
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        )

    uvicorn.run(app, host='0.0.0.0', port=8000)
