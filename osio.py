import os
cwd = os.getcwd()

"""
    Create Folder

    :param path: folder full path
    :type path: str

    returns: {status: bool, message: str}
    rtype: dict
"""


def mkdir(path):
    #print(cwd+path)
    folder = os.path.exists(cwd+path)


    if not folder:
        try:
            print("created")
            os.makedirs(cwd+path)
            return {"status": True, "message": f"{path} Created"}
        except IOError as e:
            print(e)
            return {"status": False, "message": e}

    else:
        return {"status": False, "message": "Folder Existed"}
