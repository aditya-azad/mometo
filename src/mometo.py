import json
import traceback
from collections.abc import Sequence
from os import path
from utils import error


def read_validate_config():
    try:
        with open("./mometo_config.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        error("Cannot find the config file. Please read the documentation")
    except json.decoder.JSONDecodeError:
        traceback.print_exc()
        error("Cannot read the config file, please check the syntax")
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
    optional_parameters = {
        "ingredients",
        "histidine",
        "isoleucine",
        "leucine",
        "lysine",
        "methionine",
        "phenylalanine",
        "threonine",
        "valine",
        "alanine",
        "arginine",
        "asparagine",
        "asparticacid",
        "cysteine",
        "glutamicacid",
        "glutamine",
        "glycine",
        "proline",
        "serine",
        "tyrosine",
        "fiber",
        "starch",
        "sugars",
        "monosaturated",
        "omega3",
        "omega6",
        "saturated",
        "trans",
        "cholesterol",
        "thiamine",
        "riboflavin",
        "niacin",
        "pantothenicacid",
        "pyridoxine",
        "cobalamin",
        "folate",
        "betacryptoxanthin",
        "luteinzeaxanthin",
        "vitaminc",
        "vitamind",
        "vitamine",
        "vitamink",
        "calcium",
        "copper",
        "iodine",
        "iron",
        "magnesium",
        "manganese",
        "phosphorus",
        "potassium",
        "selenium",
        "sodium",
        "zinc",
    }
    required_parameters = {
        "servingquantity",
    }
    recipes = set()
    ingredients = set()
    try:
        with open(recipes_file, "r") as file:
            data = json.load(file)
    except json.decoder.JSONDecodeError:
        traceback.print_exc()
        error("Cannot read the recipes file, please check the syntax")
    for recipe in data:
        recipes.add(recipe)
        recipe_contents = set(data[recipe].keys())
        # validate required parameters
        for param in required_parameters:
            if param not in recipe_contents:
                error(f"Cannot find \"{param}\", a required parameter for \"{recipe}\" recipe")
        # validate other parameters
        for content in recipe_contents:
            if (content not in required_parameters) and (content not in optional_parameters):
                error(f"Unrecognized ingredient \"{content}\" found in \"{recipe}\" recipe")
        # validate ingredients type
        if ("ingredients" in recipe_contents):
            if (not isinstance(data[recipe]["ingredients"], Sequence)):
                error(f"\"ingredients\" for \"{recipe}\" must be a list")
            for ingredient in data[recipe]["ingredients"]:
                ingredients.add(ingredient)
    # validate ingredients
    ingredients_not_found = set()
    for ingredient in ingredients:
        if ingredient not in recipes:
            ingredients_not_found.add(ingredient)
    if ingredients_not_found:
        ingredient_list = ", ".join(ingredients_not_found)
        error(f"Cannot find ingredient(s): {ingredient_list} in the recipes file")
    return data



def run():
    config_data = read_validate_config()
    recipes_data = read_validate_recipes_file(config_data["recipes_file"])


if __name__ == "__main__":
    run()