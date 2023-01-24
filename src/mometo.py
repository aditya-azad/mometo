import json
from os import path
from utils import error


def read_validate_config():
    try:
        with open("./mometo_config.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        error("Cannot find the config file. Please read the documentation")
    # validate recipes file
    if "recipes_file" not in data:
        error("Please have a recipes_file entry in config. Please read the documentation")
    if not data["recipes_file"].endswith(".json"):
        error("The recipes_file should be a json file")
    if not path.exists(data["recipes_file"]):
        with open(data["recipes_file"], "w") as file:
            file.write("{}")
    # validate logs dir
    if "logs_dir" not in data:
        error("Please have a logs_dir entry in config. Please read the documentation")
    if not path.isdir(data["logs_dir"]):
        error("The logs_dir entry must be a directory")
    return data


def read_validate_recipes_file(recipes_file):
    with open(recipes_file, "r") as file:
        data = json.load(file)


def run():
    config_data = read_validate_config()
    recipes_data = read_validate_recipes_file(config_data["recipes_file"])


if __name__ == "__main__":
    run()