import json


def read_setting():
    filePath = './config.json'
    with open(filePath) as f:
        json_string = json.load(f)
        print(json_string)
        settings = json_string["settings"]
        # print(json_string["settings"]["sub"])
    return settings
