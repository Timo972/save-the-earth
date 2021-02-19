import json
import zipfile
import os

def unzipFile(fileName, target):
    zip_ref = zipfile.ZipFile(fileName, 'r')
    zip_ref.extractall(target)
    zip_ref.close()

def readJson(fileName):
    if not os.path.exists(fileName):
        return None

    file = open(fileName, "r")

    content = json.load(file)
    
    file.close()
    
    return content

def writeJson(fileName, content):
    file = open(fileName, "w")

    json.dump(content, file)
    
    file.close()