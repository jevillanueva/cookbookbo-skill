from ask_sdk_core.dispatch_components import AbstractRequestHandler  # type: ignore
from ask_sdk_core.utils import is_intent_name, get_slot_value   # type: ignore
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response  # type: ignore
from ask_sdk_model.ui import SimpleCard  # type: ignore
from app.utils.lang import get_message, LANG_KEYS

RECIPE_HANDLER_INPUT = "receta" 
RECIPE_INTENT = "ObtenerReceta"

class GetRecipeIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name(RECIPE_INTENT)(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        recipe = get_slot_value(handler_input, RECIPE_HANDLER_INPUT)
        print(recipe)
        handler_input.response_builder.speak(f"Preparemos {recipe}!").set_card(
            SimpleCard(get_message(LANG_KEYS.title), f"Preparemos {recipe}!"))
        # .set_should_end_session(True)
        return handler_input.response_builder.response