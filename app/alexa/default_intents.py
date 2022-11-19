from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler,  # type: ignore
    AbstractExceptionHandler,  # type: ignore
)
from ask_sdk_core.utils import is_request_type, is_intent_name   # type: ignore
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response   # type: ignore
from ask_sdk_model.ui import SimpleCard   # type: ignore
from app.utils.lang import get_message, LANG_KEYS

class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        print("Ejecucion de la Skill.")
        speech_text = get_message(LANG_KEYS.skill_hello)
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard(get_message(LANG_KEYS.title), speech_text)
        ).set_should_end_session(False)
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        print("Ejecucion Intent Ayuda")
        speech_text = get_message(LANG_KEYS.skill_help)
        handler_input.response_builder.speak(speech_text).ask(speech_text).set_card(
            SimpleCard(get_message(LANG_KEYS.title), speech_text)
        )
        return handler_input.response_builder.response
    
class RepeatIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.RepeatIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        print("Ejecucion Intent Repeat")
        session_attributes = handler_input.attributes_manager.session_attributes
        speech_text = session_attributes['speech']
        handler_input.response_builder.speak(speech_text).ask(speech_text).set_card(
            SimpleCard(get_message(LANG_KEYS.title), speech_text)
        )
        return handler_input.response_builder.response


class CancelAndStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.CancelIntent")(handler_input) or is_intent_name(
            "AMAZON.StopIntent"
        )(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        print("Ejecucion Intent Cancel o Stop")
        speech_text = get_message(LANG_KEYS.skill_cancel)
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard(get_message(LANG_KEYS.title), speech_text)
        ).set_should_end_session(True)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # any cleanup logic goes here
        return handler_input.response_builder.response


class AllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        print(exception)
        speech = get_message(LANG_KEYS.skill_exception)
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response
