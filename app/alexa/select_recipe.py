from ask_sdk_core.dispatch_components import AbstractRequestHandler  # type: ignore
from ask_sdk_core.utils import is_intent_name, get_slot_value  # type: ignore
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response  # type: ignore
from ask_sdk_model.ui import SimpleCard  # type: ignore
from ssml_builder.core import Speech

from app.alexa.recipe_to_dialog import RecipeToSpeach
from app.alexa.speach_recipe import SpeachRecipe
from app.utils.lang import LANG_KEYS, get_message
RECIPE_HANDLER_INPUT = "option"
RECIPE_INTENT = "SeleccionarReceta"


class IntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        attr = handler_input.attributes_manager.session_attributes
        return is_intent_name(RECIPE_INTENT)(handler_input) and attr.get("in_search") == False and attr.get("in_select") == True

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        option = get_slot_value(handler_input, RECIPE_HANDLER_INPUT)
        attr = handler_input.attributes_manager.session_attributes
        recipes = attr["recipes"]
        option = int(option)
        option = option -1
        if option < len (recipes) and option >= 0:
            actual_recipe = recipes[option]
            attr["recipe"] = actual_recipe
            attr["in_search"] = False
            attr["in_select"] = False
            attr["preparation_index"] = 0
            attr["step_index"] = 0
            attr["start"] = True
            attr["init"] = True
            attr["ingredients"] = True
            attr["preparation"] = True
            attr["step"] = True
            name = actual_recipe.get("name")
            speech, display =  SpeachRecipe.speach_recipe(actual_recipe, 0,0,True, True,True, True, True)
            handler_input.response_builder.speak(speech.speech).set_card(
                SimpleCard(name, display.speech)
            ).ask(speech.speech)
        else:
            speech = Speech()
            display = Speech()
            valid_opt = get_message(LANG_KEYS.skill_options_valid)+".\n"
            speech.add_text (valid_opt)
            display.add_text (valid_opt)
            speech, display = RecipeToSpeach.recipes_to_options(speech,display, recipes)
            handler_input.response_builder.speak(speech.speech).set_card(
                SimpleCard(get_message(LANG_KEYS.skill_options_title), display.speech)
            ).ask(speech.speech)
        return handler_input.response_builder.response
