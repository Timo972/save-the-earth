import re

simplifiedSemverRegex = r"([0-9]+)\.([0-9]+)\.([0-9]+)"

"""Compares version1 with version2, returns 0 if same, 1 if two is higher and -1 if one is higher"""
def compare(version1, version2):
    # check if input is valid
    v1Match = re.match(simplifiedSemverRegex, version1)
    v2Match = re.match(simplifiedSemverRegex, version2)
    
    # if not return none
    if v1Match is None or v2Match is None:
        return None

    # split up into major, minor, patch list
    v1 = version1.split('.', 3)
    v2 = version2.split('.', 3)

    for idx, num in enumerate(v1):
        if num > v2[idx]:
            return -1
        elif num == v2[idx]:
            continue
        else:
            return 1

    return 0