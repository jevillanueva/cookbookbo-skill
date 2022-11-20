from ssml_builder.core import Speech
from app.utils.lang import get_message, LANG_KEYS


class RecipeToSpeach:
    @classmethod
    def convert_name(cls, speech: Speech, display: Speech, recipe: dict):
        start = get_message(LANG_KEYS.skill_recipe_start)
        name = recipe.get("name", "name")
        speech.add_text(start)
        speech.pause(time="0.3s")
        speech.add_text(f" {name}.\n")
        speech.pause(time="1s")

        #Screens
        display.add_text(f'{start} "{name}".\n')
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

                #Screens
                display.add_text(
                    get_message(LANG_KEYS.skill_recipe_preparation_not_principal)
                )
                display.add_text(f" {prep_name}.\n")
            else:
                speech.add_text(
                    get_message(LANG_KEYS.skill_recipe_preparation_principal)+".\n"
                )

                #Screens
                display.add_text(
                    get_message(LANG_KEYS.skill_recipe_preparation_principal)+".\n"
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
                #Screens 
                display.add_text(get_message(LANG_KEYS.skill_recipe_not_ingredients))
            else:
                title = get_message(LANG_KEYS.skill_recipe_ingredients)+"\n"
                speech.add_text(title)
                #Screens
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
                    #Screens
                    display.add_text("- "+ing_name)
                    if ing_unit == "unknow":
                        if ing_qtty_eq == 0.0:
                            speech.add_text(f" {ing_unit_eq}")
                            #Screens
                            display.add_text(f" {ing_unit_eq}")
                        elif ing_qtty_eq == int(ing_qtty_eq):
                            
                            speech.add_text(f" {int(ing_qtty_eq)} {ing_unit_eq}")
                            #Screens
                            display.add_text(f" {int(ing_qtty_eq)} {ing_unit_eq}")
                        else:
                            speech.add_text(f" {ing_qtty_eq} {ing_unit_eq}")
                            #Screens
                            display.add_text(f" {ing_qtty_eq} {ing_unit_eq}")
                    else:
                        speech.add_text(f" {ing_qtty} {ing_unit}")
                        #Screens
                        display.add_text(f" {ing_qtty} {ing_unit}")
                    if ing_optional == True:
                        unit_text = get_message(LANG_KEYS.skill_ingredient_optional)
                        speech.add_text(f" {unit_text}.")
                        #Screens
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
                #Screens
                display.add_text(get_message(LANG_KEYS.skill_recipe_not_steps))
            else:
                if len(steps) > steps_index:
                    step = steps[steps_index]
                    detail = step.get("detail", "")
                    step_pos  = steps_index +1
                    speech.say_as(step_pos, "ordinal")
                    speech.add_text(detail)
                    speech.pause(time="1s")

                    #Screens
                    display.add_text(f'{step_pos}. {detail}\n')
        return speech, display
