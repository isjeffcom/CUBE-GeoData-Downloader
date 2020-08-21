from flask import Flask
from flask import request, jsonify
from flask_cors import CORS
from downloader import DEMDownloader, OverpassJSON
from pm import pm
import time
from osio import mkdir
import json

DEM_BBOX = {
    "east": {"latitude": 55.943659895856825, "longitude": -3.1085265344946214},
    "north": {"latitude": 55.98865208029593, "longitude": -3.1888220000000005},
    "south": {"latitude": 55.89871991970406, "longitude": -3.1888220000000005},
    "west": {"latitude": 55.943659895856825, "longitude": -3.2691174655053783}
}

GEO_BBOX = {
    "east": {"latitude": 55.94368495583388, "longitude": -3.172762899971371},
    "north": {"latitude": 55.95267921605918, "longitude": -3.1888220000000005},
    "south": {"latitude": 55.9346927839408, "longitude": -3.1888220000000005},
    "west": {"latitude": 55.94368495583388, "longitude": -3.2048811000286297}
}

# overpass bbox: south, west, north, east
GEO_CONFIG = {
    "bbox": {
        "south": GEO_BBOX['south']['latitude'],
        "north": GEO_BBOX['north']['latitude'],
        "west": GEO_BBOX['west']['longitude'],
        "east": GEO_BBOX['east']['longitude']
    }
}

DEM_CONFIG = {
    "demtype": "SRTMGL1",
    "outputFormat": "GTiff",
    "south": DEM_BBOX['south']['latitude'],
    "north": DEM_BBOX['north']['latitude'],
    "west": DEM_BBOX['west']['longitude'],
    "east": DEM_BBOX['east']['longitude']
}

app = Flask(__name__, static_folder='assets', static_url_path='/assets')
CORS(app)

@app.route('/')
def main():
    return app.send_static_file("./manager/index.html")

@app.route('/all')
def all():
    p = pm()
    return json.dumps(pm.all(p))

@app.route('/del', methods=['GET', 'POST'])
def del_project():
    data = request.json
    name = data.get('name')
    pm_ins = pm()
    pm_res = pm.delete(pm_ins, name)
    if pm_res['status']:
        return json.dumps({"status": True, "message": f"Project {name} deleted, please delete file manually"})
    else:
        return json.dumps({"status": False, "message": f"Fail to delete project {name}"})


@app.route('/new', methods=['GET', 'POST'])
def new_project():
    # Current Server Timestamp
    now = int(time.time())

    data = request.json
    name = data.get('name')
    center = data.get('center')
    dem_bbox = data.get('dem_bbox')
    geo_bbox = data.get('geo_bbox')
    author = data.get('author')
    date_create = now
    date_modify = now

    # Create Folder
    mkdir(f'/assets/projects/{name}')

    GEO_CONFIG = {
        "bbox": {
            "south": geo_bbox['south']['latitude'],
            "north": geo_bbox['north']['latitude'],
            "west": geo_bbox['west']['longitude'],
            "east": geo_bbox['east']['longitude']
        }
    }

    DEM_CONFIG = {
        "demtype": "SRTMGL1",
        "outputFormat": "GTiff",
        "south": dem_bbox['south']['latitude'],
        "north": dem_bbox['north']['latitude'],
        "west": dem_bbox['west']['longitude'],
        "east": dem_bbox['east']['longitude']
    }

    pm_ins = pm()
    pm_res = pm.add(pm_ins, name, center, dem_bbox, geo_bbox, author, date_create, date_modify)

    if not pm_res['status']:
        return json.dumps(pm_res)

    # Download Data Files
    dem_res = DEMDownloader(DEM_CONFIG, name)
    building_res = OverpassJSON(GEO_CONFIG, "json", "building", name)
    water_res = OverpassJSON(GEO_CONFIG, "json", "water", name)
    highway_res = OverpassJSON(GEO_CONFIG, "json", "highway", name)

    if pm_res['status'] and dem_res["status"] and building_res["status"] and water_res["status"] and highway_res[
        "status"]:
        # Write in JSON config DB
        return json.dumps({"status": True, "message": f"Project {name} successfully created"})
    else:
        return json.dumps({"status": False,
                           "message": f"Fail to create project, Errors: {dem_res['message']} \n {building_res['message']} \n {water_res['message']} \n {highway_res['message']}"})

@app.route('/single')
def single():
    p = pm()
    name = request.args.get('name')
    return json.dumps(pm.single(p, name))


# @app.route('/upcache', methods=['GET', 'POST'])
# def cache():
#     data = request.json
#     name = data.get('name')
#     center = data.get('center')
#     return "aaa"
