import yaml


RECIPE_FILE = "recipe.yaml"

class Recipe():
    def __init__(self):
        recipe_dict = _load_yaml_file(RECIPE_FILE)
        self.recipe = recipe_dict
        self.title = recipe_dict["title"]
        self.logo = recipe_dict["logo"]
        self.favicon = recipe_dict["favicon"]
        self.entities = recipe_dict["entities"]
        self.source = recipe_dict["source"]


def _load_yaml_file(file_path):
    with open(file_path, 'r') as f:
        yml = yaml.safe_load(f)
    return yml