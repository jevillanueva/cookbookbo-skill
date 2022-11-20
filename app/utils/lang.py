from enum import Enum
import os
import traceback
import yaml


from app.core import configuration

LANG = configuration.APP_LANG
dirpath = os.path.dirname(__file__)
path = os.path.join(dirpath, "..", "lang", LANG + ".yaml")
dictionary = dict()
with open(path, encoding="utf-8") as fh:
    try:
        dictionary = yaml.safe_load(fh)
    except yaml.YAMLError as exc:
        print(exc)

class LANG_KEYS(Enum):
    default = "default"
    title = "title"
    skill_hello = "skill_hello"
    skill_help = "skill_help"
    skill_cancel = "skill_cancel"
    skill_exception = "skill_exception"

    skill_recipes_not_found = "skill_recipes_not_found"
    skill_recipe_start = "skill_recipe_start"
    skill_recipe_preparation_principal = "skill_recipe_preparation_principal"
    skill_recipe_preparation_not_principal = "skill_recipe_preparation_not_principal"
    skill_recipe_not_ingredients = "skill_recipe_not_ingredients"
    skill_recipe_ingredients = "skill_recipe_ingredients"
    # skill_ingredient_unit_singular = "skill_ingredient_unit_singular"
    # skill_ingredient_unit_many = "skill_ingredient_unit_many"
    skill_ingredient_optional = "skill_ingredient_optional"
    skill_recipe_not_steps = "skill_recipe_not_steps"

def get_message(key:LANG_KEYS):
    if not isinstance(key,LANG_KEYS):
        raise TypeError('direction must be an instance of Direction Enum')
    try:
        message = dictionary[key.value]
        return message
    except:
        try:
            traceback.print_exc()
            return dictionary[LANG_KEYS.default]
        except:
            traceback.print_exc()
            return 'Something went wrong with the dictionary "{0}"'.format(LANG)