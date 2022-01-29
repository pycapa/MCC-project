import json
import os

confg = json.dumps

def databases_conf(url):
    filename = os.path.join(url, 'db.json')
    with open(filename) as json_file:
        data = json.load(json_file)
    return data

                    