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
    skill_ingredient_optional = "skill_ingredient_optional"
    skill_recipe_not_steps = "skill_recipe_not_steps"
    skill_no_recipes = "skill_no_recipes"
    skill_select_recipe = "skill_select_recipe"
    skill_conjuntion = "skill_conjuntion"
    skill_options_title = "skill_options_title"
    skill_options_valid = "skill_options_valid"
    skill_repeat_no_init = "skill_repeat_no_init"
    skill_repeat_error = "skill_repeat_error"
    skill_next_end_recipe = "skill_next_end_recipe"
    skill_prev_init_recipe = "skill_prev_init_recipe"

    skill_recipe_init_time = "skill_recipe_init_time"
    skill_recipe_minutes = "skill_recipe_minutes"
    skill_recipe_init_portions = "skill_recipe_init_portions"
    skill_recipe_portion_single = "skill_recipe_portion_single"
    skill_recipe_portion_many = "skill_recipe_portion_many"
    skill_help_hint = "skill_help_hint"
    skill_hints_recipe =  "skill_hints_recipe"

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