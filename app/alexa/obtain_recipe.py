from ask_sdk_core.dispatch_components import AbstractRequestHandler  # type: ignore
from ask_sdk_core.utils import is_intent_name, get_slot_value  # type: ignore
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response  # type: ignore
from ask_sdk_model.ui import SimpleCard  # type: ignore
from app.utils.lang import get_message, LANG_KEYS
from app.webservices.recipes import RecipesWebService
from app.alexa.recipe_to_dialog import RecipeToSpeach
from ssml_builder.core import Speech

RECIPE_HANDLER_INPUT = "receta"
RECIPE_INTENT = "ObtenerReceta"


class IntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        attr = handler_input.attributes_manager.session_attributes
        print("======", RECIPE_INTENT)
        print(attr)
        print("======", RECIPE_INTENT)
        return (
            is_intent_name(RECIPE_INTENT)(handler_input)
            and attr.get("in_search") == True
        )

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        recipe = get_slot_value(handler_input, RECIPE_HANDLER_INPUT)
        attr = handler_input.attributes_manager.session_attributes
        print(attr)
        attr["recipe_word"] = recipe
        recipes = RecipesWebService.search_recipe(recipe)  # type: ignore

        if recipes is None or len(recipes) == 0:  # Service no work
            speak = get_message(LANG_KEYS.skill_recipes_not_found)
            handler_input.response_builder.speak(speak).set_card(
                SimpleCard(get_message(LANG_KEYS.title), speak)
            )
        else:
            if recipe is None or len(recipes) == 1:  # Random Recipe or only one recipe
                actual_recipe = recipes[0]
                attr["recipe"] = actual_recipe
                attr["in_search"] = False
                attr["in_select"] = False
                attr["preparation_index"] = 0
                attr["step_index"] = 0
                name = actual_recipe.get("name")
                speech = Speech()
                display = Speech()
                speech, display = RecipeToSpeach.convert_name(speech,display, actual_recipe)
                speech, display = RecipeToSpeach.convert_preparation(speech, display, actual_recipe, 0)
                speech, display = RecipeToSpeach.convert_ingredients(speech, display, actual_recipe, 0)
                speech, display = RecipeToSpeach.convert_steps(speech,display, actual_recipe, 0, 0)
                # speak = get_message(LANG_KEYS.skill_recipe_start)
                print(speech.speech)
                handler_input.response_builder.speak(speech.speech).set_card(
                    SimpleCard(name, display.speech)
                ).ask(speech.speech)
            else:
                # Select one recipe
                attr["in_search"] = False
                attr["in_select"] = True
                attr["recipes"] = recipes

        # .set_should_end_session(True)
        return handler_input.response_builder.response
