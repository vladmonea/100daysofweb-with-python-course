from apistar import test

from .app import app, plants, NOT_FOUND, PLANT_FAMILIES

test_client = test.TestClient(app)


def test_list_plants():
    response = test_client.get('/')
    assert response.status_code == 200

    json_resp = response.json()
    assert len(json_resp) == 1000

    expected = {
        "id": 1, "common_name": "Xanthoparmelia Lichen",
        "scientific_name": "Xanthoparmelia dissensa (T. Nash) Hale",
        "plant_family": "Parmeliaceae"
    }

    assert expected == json_resp[0]


def test_get_plant():
    response = test_client.get('/1')
    assert response.status_code == 200

    json_resp = response.json()

    expected = {
        "id": 1, "common_name": "Xanthoparmelia Lichen",
        "scientific_name": "Xanthoparmelia dissensa (T. Nash) Hale",
        "plant_family": "Parmeliaceae"
    }

    assert expected == json_resp


def test_create_plant():
    data = {
        "common_name": "Basina Porcului",
        "scientific_name": "Taraxacum officinale",
        "plant_family": "Asteraceae"
    }
    response = test_client.post('/', data=data)

    assert response.status_code == 201
    assert len(plants) == 1001

    expected = {
        "id": 1001, "common_name": "Basina Porcului",
        "scientific_name": "Taraxacum officinale",
        "plant_family": "Asteraceae"
    }
    assert response.json() == expected


def test_create_plant_invalid_family():
    data = {
        "common_name": "Pizda tigancii",
        "scientific_name": "Lamium purpureum",
        "plant_family": "Pirandae"
    }

    response = test_client.post('/', data=data)
    assert response.status_code == 400

    json_resp = response.json()
    assert json_resp["plant_family"] == f"Must be one of {list(PLANT_FAMILIES)}."


def test_create_plant_missing_fields():
    data = {
        "scientific_name": "Lamium purpureum",
        "plant_family": "Lamiaceae"
    }

    response = test_client.post('/', data=data)
    assert response.status_code == 400

    json_resp = response.json()
    assert json_resp["common_name"] == "The \"common_name\" field is required."

    data = {
        "common_name": "Pizda tigancii",
        "plant_family": "Lamiaceae"
    }

    response = test_client.post('/', data=data)
    assert response.status_code == 400

    json_resp = response.json()
    assert json_resp["scientific_name"] == "The \"scientific_name\" field is required."

    data = {
        "common_name": "Pizda tigancii",
        "scientific_name": "Lamium purpureum"
    }

    response = test_client.post('/', data=data)
    assert response.status_code == 400

    json_resp = response.json()
    assert json_resp["plant_family"] == "The \"plant_family\" field is required."


def test_update_plant():
    data = {
        "common_name": "Covfefe River Colicwood",
        "scientific_name": "Myrsine mezii Hosaka",
        "plant_family": "Myrsinaceae"
    }
    response = test_client.put('/42', data=data)
    assert response.status_code == 200

    expected = {
        "id": 42,
        "common_name": "Covfefe River Colicwood",
        "scientific_name": "Myrsine mezii Hosaka",
        "plant_family": "Myrsinaceae"
    }
    assert response.json() == expected


def test_update_plant_missing_fields():
    data = {
        "common_name": "Covfefe River Colicwood",
        "scientific_name": "Myrsine mezii Hosaka",
    }
    response = test_client.put('/42', data=data)
    assert response.status_code == 400


def test_delete():
    response = test_client.delete('/1001')
    json_resp = response.json()

    assert response.status_code == 204
    assert json_resp == {}


def test_delete_nonexistent_id():
    response = test_client.delete('/100001')

    assert response.status_code == 404
