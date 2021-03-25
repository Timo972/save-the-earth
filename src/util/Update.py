import json

from File import *
from Version import *
from Fetch import *

def check():
    print("checking for update")
    url = "https://cdn.timosengine.cf/save-the-earth/version.json"

    #fetchUrl("cdn.timosengine.cf", 80, "/save-the-earth/version.json")
    responseStr = fetchUrl(url)

    print("fetched url")

    if responseStr is None:
        return False

    response = json.loads(responseStr)

    localVersion = readJson("version.json")

    localVersion = localVersion["version"] if not localVersion is None else None

    latestVersion = response["version"][1:] if not response is None else localVersion

    status = compare(localVersion, latestVersion)

    print("version status: {}".format(status))

    return status > 0

def update():
    print("update")
    url = "https://cdn.timosengine.cf/save-the-earth/SaveTheEarth.zip"
    return True