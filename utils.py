import json
import os
from urllib.parse import unquote


def get_filename(url):
    # 1 way mapping from url to a page in the file system

    return "../pages/" + "/".join(url.split("/")[2:])


def get_nice_name(name):
    # 1 way mapping from url or filename to a more nice name
    return unquote(os.path.split(name)[1]).replace('_', ' ')


def load_model(base_url):
    # loads in the model from the file system

    with open(get_filename(base_url + "/indices.json"), "r") as f:
        index = json.loads(f.read())
        print("Model successfully loaded in")
    return index
