import yaml
from pathlib import Path


def load_yaml(path):
    return yaml.load(open(Path(path), "r"), Loader=yaml.FullLoader)


def save_yaml(obj, path):
    yaml.dump(obj, open(Path(path), "w"))