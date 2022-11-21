from typing import List
from ssml_builder.core import Speech
from app.utils.lang import get_message, LANG_KEYS


class RecipeToSpeach:
    @classmethod
    def convert_name(cls, speech: Speech, display: Speech, recipe: dict):
        start = get_message(LANG_KEYS.skill_recipe_start)
        name = recipe.get("name", "name")
        speech.add_text(start)
        speech.pause(time="0.3s")
        conjuntion = get_message(LANG_KEYS.skill_conjuntion)

        owner = recipe.get("owner", None)
        publisher = recipe.get("publisher", None)
        if owner is not None:
            name_text = f' "{name}" {conjuntion} {owner}.\n'
        elif publisher is not None:
            name_text = f' "{name}" {conjuntion} {publisher}.\n'
        else:
            name_text = f' "{name}".\n'
        speech.add_text(name_text)

        speech.pause(time="1s")

        init_time = get_message(LANG_KEYS.skill_recipe_init_time)
        time = recipe.get("preparation_time_minutes", 0)
        end_time = get_message(LANG_KEYS.skill_recipe_minutes)
        total_time = f"{init_time} {time} {end_time}.\n"
        speech.add_text(total_time)

        init_portion = get_message(LANG_KEYS.skill_recipe_init_portions)
        portions = recipe.get("portion", 0)
        if portions == 1:
            end_portion = get_message(LANG_KEYS.skill_recipe_portion_single)
        else:
            end_portion = get_message(LANG_KEYS.skill_recipe_portion_many)
        total_portions = f"{init_portion} {portions} {end_portion}.\n"
        speech.add_text(total_portions)
        speech.pause(time="0.5s")

        # Screens
        display.add_text(f"{start} {name_text}")
        display.add_text(total_time)
        display.add_text(total_portions)
        return speech, display

    @classmethod
    def convert_preparation(
        cls, speech: Speech, display: Speech, recipe: dict, preparation_index: int = 0
    ):
        preparations = recipe.get("preparation", [])
        if len(preparations) > preparation_index:
            preparation = preparations[preparation_index]
            prep_name = preparation.get("name", "principal")
            if prep_name.lower() != "principal".lower():
                speech.add_text(
                    get_message(LANG_KEYS.skill_recipe_preparation_not_principal)
                )
                speech.add_text(f" {prep_name}.\n")

                # Screens
                display.add_text(
                    get_message(LANG_KEYS.skill_recipe_preparation_not_principal)
                )
                display.add_text(f" {prep_name}.\n")
            else:
                speech.add_text(
                    get_message(LANG_KEYS.skill_recipe_preparation_principal) + ".\n"
                )

                # Screens
                display.add_text(
                    get_message(LANG_KEYS.skill_recipe_preparation_principal) + ".\n"
                )
        return speech, display

    @classmethod
    def convert_ingredients(
        cls, speech: Speech, display: Speech, recipe: dict, preparation_index: int = 0
    ):
        preparations = recipe.get("preparation", [])
        if len(preparations) > preparation_index:
            preparation = preparations[preparation_index]
            ingredients = preparation.get("ingredients", [])
            if len(ingredients) == 0:
                speech.add_text(get_message(LANG_KEYS.skill_recipe_not_ingredients))
                # Screens
                display.add_text(get_message(LANG_KEYS.skill_recipe_not_ingredients))
            else:
                title = get_message(LANG_KEYS.skill_recipe_ingredients) + "\n"
                speech.add_text(title)
                # Screens
                display.add_text(title)
                for ingredient in ingredients:
                    ing_name = ingredient.get("name", "")
                    ing_qtty = ingredient.get("quantity_si", 0.0)
                    ing_unit = ingredient.get("unit_si", "")
                    ing_qtty = ingredient.get("quantity_si", 0.0)

                    ing_optional = ingredient.get("optional", False)

                    ing_qtty_eq = ingredient.get("quantity_equivalence", 0.0)
                    ing_unit_eq = ingredient.get("unit_equivalence", "")

                    speech.add_text(ing_name)
                    # Screens
                    display.add_text("- " + ing_name)
                    if ing_unit == "unknow":
                        if ing_qtty_eq == 0.0:
                            speech.add_text(f" {ing_unit_eq}")
                            # Screens
                            display.add_text(f" {ing_unit_eq}")
                        elif ing_qtty_eq == int(ing_qtty_eq):

                            speech.add_text(f" {int(ing_qtty_eq)} {ing_unit_eq}")
                            # Screens
                            display.add_text(f" {int(ing_qtty_eq)} {ing_unit_eq}")
                        else:
                            speech.add_text(f" {ing_qtty_eq} {ing_unit_eq}")
                            # Screens
                            display.add_text(f" {ing_qtty_eq} {ing_unit_eq}")
                    else:
                        speech.add_text(f" {ing_qtty} {ing_unit}")
                        # Screens
                        display.add_text(f" {ing_qtty} {ing_unit}")
                    if ing_optional == True:
                        unit_text = get_message(LANG_KEYS.skill_ingredient_optional)
                        speech.add_text(f" {unit_text}.")
                        # Screens
                        display.add_text(f" {unit_text}.")
                    speech.pause(time="1s")
                    speech.add_text("\n")
                    display.add_text("\n")
        return speech, display

    @classmethod
    def convert_steps(
        cls,
        speech: Speech,
        display: Speech,
        recipe: dict,
        preparation_index: int = 0,
        steps_index: int = 0,
    ):
        preparations = recipe.get("preparation", [])
        if len(preparations) > preparation_index:
            preparation = preparations[preparation_index]
            steps = preparation.get("steps", [])
            if len(steps) == 0:
                speech.add_text(get_message(LANG_KEYS.skill_recipe_not_steps))
                # Screens
                display.add_text(get_message(LANG_KEYS.skill_recipe_not_steps))
            else:
                if len(steps) > steps_index:
                    step = steps[steps_index]
                    detail = step.get("detail", "")
                    step_pos = steps_index + 1
                    speech.say_as(step_pos, "ordinal")
                    speech.add_text(f". {detail}")
                    speech.pause(time="1s")

                    # Screens
                    display.add_text(f"{step_pos}. {detail}\n")
        return speech, display

    @classmethod
    def recipes_to_options(cls, speech: Speech, display: Speech, recipes: List[dict]):
        if len(recipes) == 0:
            speech.add_text(get_message(LANG_KEYS.skill_no_recipes))
            # Screens
            display.add_text(get_message(LANG_KEYS.skill_no_recipes))
        else:
            select = get_message(LANG_KEYS.skill_select_recipe) + ":\n"
            speech.add_text(select)
            display.add_text(select)
            conjuntion = get_message(LANG_KEYS.skill_conjuntion)
            for idx, recipe in enumerate(recipes):
                name = recipe.get("name", "")
                owner = recipe.get("owner", None)
                publisher = recipe.get("publisher", None)
                speech.say_as(idx + 1, "cardinal")
                display.add_text(f"{idx+1}. ")
                if owner is not None:
                    option = f" {name} {conjuntion} {owner}.\n"
                    speech.add_text(option)
                    display.add_text(option)
                elif publisher is not None:
                    option = f" {name} {conjuntion} {publisher}.\n"
                    speech.add_text(option)
                    display.add_text(option)
                else:
                    option = f" {name}.\n"
                    speech.add_text(option)
                    display.add_text(option)
        return speech, display
