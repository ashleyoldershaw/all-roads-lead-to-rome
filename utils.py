import json


def get_filename(url):
    # 1 way mapping from url to a page in the file system

    filename = "pages/" + "/".join(url.split("/")[2:])

    protected_pages = ["index","iso", "example.webscraping.com"]

    for name in protected_pages:
        if name in filename and not filename.endswith(name):
            filename = filename.replace(name,"{}_dir".format(name))

    return filename


def load_model(base_url):
    # loads in the model from the file system

    with open(get_filename(base_url + "/indices.json"), "r") as f:
        index = json.loads(f.read())
        print("Model successfully loaded in")
    return index
