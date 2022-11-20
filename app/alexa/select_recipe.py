from ask_sdk_core.dispatch_components import AbstractRequestHandler  # type: ignore
from ask_sdk_core.utils import is_intent_name, get_slot_value  # type: ignore
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response  # type: ignore
from ask_sdk_model.ui import SimpleCard  # type: ignore
from app.utils.lang import get_message, LANG_KEYS
from app.webservices.recipes import RecipesWebService

RECIPE_HANDLER_INPUT = "option"
RECIPE_INTENT = "SeleccionarReceta"


class IntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        attr = handler_input.attributes_manager.session_attributes
        print ("======", RECIPE_INTENT )
        print (attr)
        print ("======", RECIPE_INTENT )
        return is_intent_name(RECIPE_INTENT)(handler_input) and attr.get("in_search") == False and attr.get("in_select") == True

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        recipe = get_slot_value(handler_input, RECIPE_HANDLER_INPUT)
        attr = handler_input.attributes_manager.session_attributes
        print(attr)
        attr["recipe_word"] = recipe
        attr["preparation"] = False
        recipes = RecipesWebService.search_recipe(recipe)  # type: ignore

        if recipes is None or len(recipes) == 0:  # Service no work
            speak = get_message(LANG_KEYS.skill_recipes_not_found)
            handler_input.response_builder.speak(speak).set_card(
                SimpleCard(get_message(LANG_KEYS.title), speak)
            )
        else:
            if recipe is None:  # Random Recipe
                actual_recipe = recipes[0]
                attr["recipe"] = actual_recipe
                name = actual_recipe.get("name")
                speak = get_message(LANG_KEYS.skill_recipe_start)
                handler_input.response_builder.speak(f"{speak} {name}").set_card(
                    SimpleCard(get_message(LANG_KEYS.title), f"{speak} {name}")
                ).ask(get_message(LANG_KEYS.skill_recipe_ask_confirm))
            else:
                # Select one recipe
                attr["recipes"] = recipes

        # .set_should_end_session(True)
        return handler_input.response_builder.response
