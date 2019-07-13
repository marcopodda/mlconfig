import yaml
from pathlib import Path


def load_yaml(path):
    path = Path(path)
    return yaml.load(open(path, "r"), Loader=yaml.FullLoader)

def save_yaml(obj, path):
    path = Path(path)
    yaml.dump(obj, open(path, "w"))