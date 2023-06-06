import json
import requests
from pathlib import Path

try:
    import anki_sdk.utils as utils
    import anki_sdk.exceptions as exceptions
    import anki_sdk.controllers as controllers
    import anki_sdk.cars as cars
    import anki_sdk.api as api
except ModuleNotFoundError:
    import utils
    import exceptions
    import controllers
    import cars
    import api

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
        
try:
    path = getPath()
    data = getData(path)
    extra = getExtra(path)
    all_data = loadAll(path)


    __version__ = data["version"]
    __desc__ = data["desc"]
    __link__ = data["link"]
    __update__ = extra["download"]
except Exception as e:
    pass


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
    