from ssml_builder.core import Speech

from app.alexa.recipe_to_dialog import RecipeToSpeach


class SpeachRecipe:
    @classmethod
    def speach_recipe(
        cls,
        recipe: dict,
        preparation_idx: int = 0,
        step_idx: int = 0,
        ingredients: bool = False,
        init: bool = False,
        preparation: bool = False,
        step: bool = False,
        hint: bool = False
    ):
        speech = Speech()
        display = Speech()
        if init == True:
            speech, display = RecipeToSpeach.convert_name(speech, display, recipe)
        if preparation == True:
            speech, display = RecipeToSpeach.convert_preparation(speech, display, recipe, preparation_idx)
        if ingredients == True:
            speech, display = RecipeToSpeach.convert_ingredients(speech, display, recipe, preparation_idx)
        if step == True:
            speech, display = RecipeToSpeach.convert_steps(speech, display, recipe, preparation_idx, step_idx)
        if hint == True:
            speech, display = RecipeToSpeach.convert_hints(speech, display)
        return speech,display
