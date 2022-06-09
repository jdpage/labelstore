import labelstore
import pytest
import uuid


@pytest.fixture()
def store():
    return labelstore.item.store


@pytest.fixture()
def app(store):
    labelstore.app.config.update(
        {
            "TESTING": True,
        }
    )
    yield labelstore.app
    store.clear()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_create(client):
    response = client.post("/item", json={"label": "hello, world!"})
    assert 201 == response.status_code
    item = response.get_json()
    assert "hello, world!" == item["label"]


def test_create_missing_label(client):
    response = client.post("/item", json={"not a label": "oh no"})
    assert 400 == response.status_code


def test_fetch_item(store, client):
    id, expected_item = store.create("hello, world")
    response = client.get(f"/item/{id}")
    assert 200 == response.status_code
    actual_item = response.get_json()
    assert id == actual_item["id"]
    assert "hello, world" == actual_item["label"]
    assert expected_item.create_ts.isoformat() == actual_item["ts"]


def test_fetch_missing_item(client):
    bad_id = uuid.uuid4().hex
    response = client.get(f"/item/{bad_id}")
    assert 404 == response.status_code


def test_all_returns_empty(client):
    response = client.get("/item/all")
    assert 200 == response.status_code
    assert response.get_json() == []


def test_all_returns_all(store, client):
    store.create("foo")
    store.create("bar")
    store.create("baz")
    response = client.get("/item/all")
    assert 200 == response.status_code
    assert {"foo", "bar", "baz"} == {item["label"] for item in response.get_json()}


def test_random_id_matches(store, client):
    labels = {"foo", "bar", "baz", "spam", "eggs"}
    label_ids = {
        item.label: id for id, item in (store.create(label) for label in labels)
    }

    for _ in range(20):
        response = client.get("/item/random")
        assert 200 == response.status_code
        item = response.get_json()
        assert label_ids[item["label"]] == item["id"]


def test_random_with_empty_fails_gracefully(client):
    response = client.get("/item/random")
    assert 404 == response.status_code
