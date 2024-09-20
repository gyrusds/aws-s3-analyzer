import os
import json
import logging
import uvicorn
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, status
from dotenv import load_dotenv


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
    """
    Retrieves the summary from a JSON file located in the output folder specified by the environment variable 'OUTPUT_FOLDER'.

    Returns:
        dict: The contents of the summary JSON file if it exists.

    Raises:
        FileNotFoundError: If the summary JSON file does not exist, logs the error and returns an ORJSONResponse with a 404 status code and an error message.

    Note:
        The function expects the environment variable 'OUTPUT_FOLDER' to be set and pointing to the directory containing the 'summary.json' file.
    """

    try:
        with open(f"{os.environ['OUTPUT_FOLDER']}/summary.json", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError as ex:
        logging.error(ex)
        return ORJSONResponse(content={"error": "There is no summary"}, status_code=status.HTTP_404_NOT_FOUND)


@app.get("/{bucket_name}")
def get_bucket(bucket_name: str):
    """
    Retrieves the contents of a JSON file corresponding to the specified S3 bucket.

    This function attempts to open and read a JSON file located in the directory specified
    by the 'OUTPUT_FOLDER' environment variable. The file name is expected to be the bucket
    name with a '.json' extension. If the file is found, its contents are returned as a
    Python dictionary. If the file is not found, an error is logged and an ORJSONResponse
    with a 404 status code is returned.

    Args:
        bucket_name (str): The name of the S3 bucket.

    Returns:
        dict: The contents of the JSON file if found.
        ORJSONResponse: An error response if the file is not found.
    """

    try:
        with open(f"{os.environ['OUTPUT_FOLDER']}/{bucket_name}.json", encoding="utf-8") as f:
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
