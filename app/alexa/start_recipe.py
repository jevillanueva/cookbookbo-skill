from ask_sdk_core.dispatch_components import AbstractRequestHandler  # type: ignore
from ask_sdk_core.utils import is_intent_name, get_slot_value, get_slot  # type: ignore
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response  # type: ignore
from ask_sdk_model.ui import SimpleCard  # type: ignore
from app.utils.lang import get_message, LANG_KEYS
from app.webservices.recipes import RecipesWebService

RECIPE_HANDLER_INPUT = "confirmation"
RECIPE_INTENT = "IniciarReceta"


class IntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        attr = handler_input.attributes_manager.session_attributes
        print ("======", RECIPE_INTENT )
        print (attr)
        print ("======", RECIPE_INTENT )
        return is_intent_name(RECIPE_INTENT)(handler_input) and attr.get("in_search") == False and attr.get("in_select") == False

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        confirm = get_slot(handler_input, RECIPE_HANDLER_INPUT)
        resolutions.resolutions_per_authority[0].values[0].value.id
        print (confirm)
        attr = handler_input.attributes_manager.session_attributes
        print(attr)
        attr["preparation"] = True
        recipe = attr["recipe"]
        speak = recipe.get("name")
        handler_input.response_builder.speak(speak).set_card(
            SimpleCard(get_message(LANG_KEYS.title), speak)
        )
        return handler_input.response_builder.response
