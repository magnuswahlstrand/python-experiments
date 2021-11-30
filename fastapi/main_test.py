from fastapi.testclient import TestClient

import main


def test_read_items():
    with TestClient(main.app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"Hello": "World"}


def test_path_param_error_if_not_int():
    with TestClient(main.app) as client:
        response = client.get("/items/foo")
        assert response.status_code == 422


def test_enum_route_errors_if_not_enum():
    with TestClient(main.app) as client:
        response = client.get("/models/bar")
        assert response.status_code == 422


def test_enum_route_ok():
    with TestClient(main.app) as client:
        response = client.get("/models/resnet")
        assert response.status_code == 200


def test_query_param():
    with TestClient(main.app) as client:
        response = client.get("/query", params={"q": 10})
        assert response.status_code == 200
        assert response.json() == 10
