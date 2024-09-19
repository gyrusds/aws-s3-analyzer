import os
import json
from src.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_summary():
    os.environ['OUTPUT_FOLDER'] = 'tests/data'

    response = client.get("/")
    assert response.status_code == 200
    with open(f"{os.environ['OUTPUT_FOLDER']}/summary.json") as f:
        assert response.json() == json.load(f)


def test_summary_wrong():
    os.environ['OUTPUT_FOLDER'] = 'wrong_folder'

    response = client.get("/")
    assert response.status_code == 404


def test_bucket():
    os.environ['OUTPUT_FOLDER'] = 'tests/data'

    response = client.get("/foo-bar")
    assert response.status_code == 200
    with open(f"{os.environ['OUTPUT_FOLDER']}/foo-bar.json") as f:
        assert response.json() == json.load(f)


def test_bucket_wrong():
    os.environ['OUTPUT_FOLDER'] = 'tests/data'

    response = client.get("/wrong_bucket")
    assert response.status_code == 404
