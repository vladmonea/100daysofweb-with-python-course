import json

from apistar import validators, types, App, Route
from apistar.http import JSONResponse


def _load_data():
    with open('plants.json', encoding='utf-8') as fobj:
        plants = json.loads(fobj.read())
        return {plant["id"]: plant for plant in plants}


plants = _load_data()
PLANT_FAMILIES = {plant["plant_family"] for plant in plants.values()}
NOT_FOUND = "Plant {} not found"


class Plant(types.Type):
    id = validators.Integer(minimum=0, allow_null=True)
    common_name = validators.String(min_length=3, max_length=50)
    scientific_name = validators.String(min_length=5)
    plant_family = validators.String(enum=list(PLANT_FAMILIES))


def list_plants():
    return [Plant(plant) for idx, plant in sorted(plants.items())]


def create_plant(plant: Plant) -> JSONResponse:
    plant_id = len(plants) + 1
    plant.id = plant_id
    plants[plant_id] = plant
    return JSONResponse(Plant(plant), status_code=201)


def get_plant(plant_id: int) -> JSONResponse:
    if plant_id not in plants:
        error = {"error": NOT_FOUND.format(plant.id)}
        return JSONResponse(error, status_code=404)

    return JSONResponse(plants[plant_id], status_code=200)


def update_plant(plant_id: int, plant: Plant) -> JSONResponse:
    if plant_id not in plants:
        error = {"error": NOT_FOUND.format(plant.id)}
        return JSONResponse(error, status_code=404)

    plant.id = plant_id
    for key, value in plant.items():
        plants[plant_id][key] = value
    return JSONResponse(Plant(plants[plant_id]), status_code=200)


def delete_plant(plant_id: int) -> JSONResponse:
    if plant_id not in plants:
        error = {"error": NOT_FOUND.format(plant_id)}
        return JSONResponse(error, status_code=404)

    del plants[plant_id]
    return JSONResponse({}, status_code=204)


routes = [
    Route('/', method="get", handler=list_plants),
    Route('/', method="post", handler=create_plant),
    Route('/{plant_id}', method="get", handler=get_plant),
    Route('/{plant_id}', method="put", handler=update_plant),
    Route('/{plant_id}', method="delete", handler=delete_plant)
]


app = App(routes=routes)


if __name__ == "__main__":
    app.serve('127.0.0.1', 5000, debug=True)
