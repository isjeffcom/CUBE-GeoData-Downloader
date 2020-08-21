import json
import os
import copy

ALL_PROJECT = {
    "App": "CUBE Data Visualisation",
    "Developer": "Jeff Wu",
    "Email": "hello@isjeff.com",
    "Repo": "https://github.com/isjeffcom/CUBE-Data-Visualization",
    "Projects": []
}

SINGLE_PROJECT = {
    "name": "",
    "center": "",
    "dem_bbox": "",
    "geo_bbox": "",
    "dir": "/",
    "author": "",
    "date_create": "",
    "date_modify": "",
    "cache_building": False,
    "cache_road": False
}

cwd = os.getcwd()
path = cwd + '/projects.json'


class pm:

    def __init__(self):
        self.content = read()

    def all(self):
        return self.content

    def single(self, name):
        index = self.search(name)
        if index != -1:
            return self.content['projects'][index]
        else:
            return False


    """
        Add a new project

        :param name: project name
        :type name: str
        :param center: Geo center {latitude: Number, longitude: Number}
        :type center: str as dict
        ...

        returns: True -> No existed project allow continue, False -> Project existed stop
        rtype: bool
    """

    def add(self, name, center, dem_bbox, geo_bbox, author, date_create, date_modify):
        if not name:
            return {"status": False, "message": f"No Project Name Imported"}

        if config_checker():
            # If same name
            print(check_name(name))
            if not check_name(name):
                print("aaa")
                return {"status": False, "message": f"Project Existed"}

            # Copy content
            content = copy.copy(self.content)

            # New Project() constructor
            new = Project(name, center, dem_bbox, geo_bbox, author, date_create, date_modify)

            # Convert dict to .Json format
            #j = json.dumps()

            # Add to projects children
            content['projects'].append(new.__dict__)

            # Check if write file success
            if write(content):
                return {"status": True, "message": f"Project {name} Created"}
            else:
                return {"status": False, "message": f"Fail to add {name} project"}

    # Delete project
    def delete(self, name):
        if not name:
            return {"status": False, "message": "No Project Name Imported"}

        search_res = self.search(name)
        # Search for project
        if search_res != -1:

            # Copy content
            content = copy.copy(self.content)

            # Remove from array
            del content['projects'][search_res]

            # Check if write file success
            if write(content):
                return {"status": True, "message": f"Project {name} Deleted"}
            else:
                return {"status": False, "message": f"Fail to Delete {name} Project"}

        else:
            return {"status": False, "message": "Project not found, did nothing"}

    def search(self, name):
        if not name:
            return -1

        i = 0
        for item in self.content['projects']:
            if item['name'] == name:
                return i
            i = i + 1

        return -1


class Project:
    def __init__(self, name, center, dem_bbox, geo_bbox, author, date_create, date_modify):
        self.name = name
        self.center = center
        self.dem_bbox = dem_bbox
        self.geo_bbox = geo_bbox
        self.author = author
        self.date_create = date_create
        self.date_modify = date_modify
        self.cache_building = False
        self.cache_road = False

    def update_name(self, name):
        self.name = name

    def update_bbox(self, bbox_type, data):
        if bbox_type == "dem":
            self.dem_bbox = data

        if bbox_type == "geo":
            self.geo_bbox = data


def config_checker():
    if not os.path.exists(path):
        try:
            write(ALL_PROJECT)
            return True

        except IOError as e:
            print("projects.json does not exist and can not be created. Permissions needed.")
            print(e)
            return False
    else:
        return True


"""
    Check if name existed in projects
    
    :param name: project name
    :type name: str
    
    returns: True -> No existed project allow continue, False -> Project existed stop
    rtype: bool
"""


def check_name(name):
    content = read()
    if len(content['projects']) == 0:
        return True

    for item in content['projects']:
        if item['name'] == name:
            return False

    return True


''' 
    Get all content in json 

    returns: return content if success, return False if fail
    rtype: any
'''


def read():
    try:
        with open(path, 'r') as f:
            content = json.load(f)
            f.close()
            return content

    except IOError as e:
        print("projects.json is not readable. Permissions needed.")
        print(e)
        return False


''' 
    Write assets into projects.json
    
    :param assets: dict waiting to write into json file
    :type assets: dict

    returns: True -> Write successful, False -> No permission or other error
    rtype: bool
'''


def write(data):
    s = json.dumps(data)
    try:
        with open(path, 'w') as f:
            f.write(s)
            f.close()
            return True

    except IOError as e:
        print("projects.json is not writeable. Permissions needed.")
        print(e)
        return False
