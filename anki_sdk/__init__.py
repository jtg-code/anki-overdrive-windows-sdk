import json
import requests
from pathlib import Path

# def getPath():
#     main = __file__
#     main = main.removesuffix("__init__.py")
#     return main

def getPath():
    main = Path(__file__).resolve().parent.parent
    return main

def getData(path):
    f = open(f"{path}/files/metadata.json", "r")
    data = json.load(f)
    f.close()
    return data["data"]

def getExtra(path):
    f = open(f"{path}/files/metadata.json", "r")
    data = json.load(f)
    f.close()
    return data["extra"]

def loadAll(path):
    with open(f"{path}/files/metadata.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        return data
        
path = getPath()
data = getData(path)
extra = getExtra(path)
all_data = loadAll(path)


__version__ = data["version"]
__desc__ = data["desc"]
__link__ = data["link"]
__update__ = extra["download"]


def checkVersion(version):
    check = requests.get(extra["update"]).text
    check = json.load(check)
    if str(check["data"]["version"]).casefold() == str(version).casefold():
        return True, check["data"]["version"]
    else:
        return False, check["data"]["version"]

if __name__ == '__main__':
    current, version = checkVersion(__version__)
    if not current:
        print(f"Update available: {__version__} -> {version}")
    