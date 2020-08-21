import requests
import codecs
import osm2geojson
import json
import os
from urllib.parse import quote

BASE_DEM = 'https://portal.opentopography.org/API/globaldem'
BASE_OVERPASS = "http://overpass-api.de/api/interpreter"

cwd = os.getcwd()


def DEMDownloader(config, pname):
    # ID Target Download Path
    tar_path = cwd + f'/assets/projects/{pname}'

    # Make sure path exist
    if not os.path.exists(tar_path):
        return {"status": False, "message": "Folder not exist"}

    url = constParam(BASE_DEM, config)
    print(url)
    req = requests.get(url)

    if req.status_code == 200:
        try:
            with open(tar_path + '/terrain.tif', 'wb') as f:
                f.write(req.content)
                f.close()
                print('File downloaded')
                return {"status": True, "message": "DEM Tiff Successfully downlaoded"}
        except IOError as e:
            print('File Write Error')
            return {"status": False, "message": "Save File Error"}
    else:
        return {"status": False, "message": f"Download {pname} DEM Internet Connection Error"}


def OverpassJSON(config, ret_format, req_type, pname):
    # Path
    cache_path = cwd + f'/assets/projects/{pname}'

    # Make sure path exist
    if not os.path.exists(cache_path):
        return {"status": False, "message": "Folder not existed"}

    url = constOverpassQL(BASE_OVERPASS, ret_format, 30, req_type, config['bbox'])

    req = requests.get(url)

    if req.status_code == 200:
        cache_path = cwd + f'/assets/projects/{pname}/{req_type}'
        try:
            with open(cache_path + '.json', 'wb') as f:
                f.write(req.content)
                f.close()
                convertGeoJson(cache_path + '.json', cache_path + '.geojson')
                return {"status": True, "message": "OSM json successfully downloaded"}

        except IOError as e:
            print('Building GeoJson Error')
            return {"status": False, "message": "Save Building GeoJson Error"}


    else:
        return {"status": False, "message": f"Download {req_type} JSON Internet Connection Error"}


def convertGeoJson(in_path, out_path):
    with codecs.open(in_path, 'r', encoding='utf-8') as data:
        js = data.read()

    geojson = osm2geojson.json2geojson(js)
    s = json.dumps(geojson)
    s = s.encode()
    with open(out_path, 'wb') as f:
        f.write(s)
        f.close()
        return {"status": True, "message": "GeoJson Convert Successful"}


def constParam(api, param):
    res = api
    i = 0
    for key, value in param.items():
        value = str(value)
        if i == 0:
            res = res + '?' + key + '=' + value + '&'
        elif i == len(param) - 1:
            res = res + key + '=' + value
        else:
            res = res + key + '=' + value + '&'

        i = i + 1

    return res


def constOverpassQL(api, output, timeout, query_type, bbox):
    if not query_type:
        return False

    query = f'[out:{output}][timeout:{timeout}];'

    b = f'({bbox["south"]}, {bbox["west"]}, {bbox["north"]}, {bbox["east"]})'
    if query_type == 'building':
        query += f'(way["building"]{b};' \
                 f'relation["building"]["type"="multipolygon"]{b};' \
                 ');'

    if query_type == 'highway':
        query += f'(way["highway"]{b};' \
                 ');'

    if query_type == 'water':
        query += f'(way["natural"="water"]{b};' \
                 f'relation["natural"="water"]{b};' \
                 f'way["waterway"]{b};' \
                 ');'

    query += 'out;>;out qt;'
    # print(query)
    return BASE_OVERPASS + '?data=' + quote(query, 'utf-8')
    # return quote(query, 'utf-8')
