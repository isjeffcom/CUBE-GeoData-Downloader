
# SAVE FOR FUTURE

# GEO_BBOX = {
#     'east': {'latitude': 55.94368495583388, 'longitude': -3.172762899971371},
#     'north': {'latitude': 55.95267921605918, 'longitude': -3.1888220000000005},
#     'south': {'latitude': 55.9346927839408, 'longitude': -3.1888220000000005},
#     'west': {'latitude': 55.94368495583388, 'longitude': -3.2048811000286297}
# }

class bbox:
    def __init__(self, east, north, south, west):
        self.east = east
        self.north = north
        self.south = south
        self.west = west

class coor:
    def __init__(self, lat, lon):
        self.latitude = lat
        self.longitude = lon