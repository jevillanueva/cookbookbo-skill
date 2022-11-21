from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler,  # type: ignore
    AbstractExceptionHandler,  # type: ignore
)
from ask_sdk_core.utils import is_request_type, is_intent_name  # type: ignore
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response  # type: ignore
from ask_sdk_model.ui import SimpleCard
from app.alexa.speach_recipe import SpeachRecipe  # type: ignore
from app.utils.lang import get_message, LANG_KEYS


class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        attr = handler_input.attributes_manager.session_attributes
        attr["in_search"] = True
        speech_text = get_message(LANG_KEYS.skill_hello)
        handler_input.response_builder.speak(speech_text).speak(speech_text).set_card(
            SimpleCard(get_message(LANG_KEYS.title), speech_text)
        ).set_should_end_session(False)
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = get_message(LANG_KEYS.skill_help)
        handler_input.response_builder.speak(speech_text).ask(speech_text).set_card(
            SimpleCard(get_message(LANG_KEYS.title), speech_text)
        )
        return handler_input.response_builder.response


class RepeatIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        attr = handler_input.attributes_manager.session_attributes
        return is_intent_name("AMAZON.RepeatIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        attr = handler_input.attributes_manager.session_attributes
        if attr.get("start") == True:

            start = attr.get("start", False)
            init = attr.get("init", False)
            ingredients = attr.get("ingredients", False)
            preparation = attr.get("preparation", False)
            step = attr.get("step", False)
            prep_idx = attr.get("preparation_index", 0)
            step_idx = attr.get("step_index", 0)
            recipe = attr.get("recipe", {"name": ""})
            name = recipe.get("name")
            speech, display = SpeachRecipe.speach_recipe(
                recipe, prep_idx, step_idx, ingredients, init,preparation, step
            )
            handler_input.response_builder.speak(speech.speech).set_card(
                SimpleCard(name, display.speech)
            ).ask(speech.speech)

        else:
            in_search = attr.get("in_search")
            in_select = attr.get("in_select")
            if in_search == True or in_select == True:
                speak = get_message(LANG_KEYS.skill_repeat_no_init)
                handler_input.response_builder.speak(speak).set_card(
                    SimpleCard(get_message(LANG_KEYS.title), speak)
                ).ask(speak)
            else:
                speak = get_message(LANG_KEYS.skill_repeat_error)
                handler_input.response_builder.speak(speak).set_card(
                    SimpleCard(get_message(LANG_KEYS.title), speak)
                ).ask(speak)
        return handler_input.response_builder.response

class NextIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        attr = handler_input.attributes_manager.session_attributes
        return is_intent_name("AMAZON.NextIntent")(handler_input) and attr.get("start", False) == True

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        attr = handler_input.attributes_manager.session_attributes
        
        preparation_state = attr.get("preparation", False)
        init = attr.get("init", False)
        ingredients = attr.get("ingredients", False)
        step = attr.get("step", False)
        prep_idx = attr.get("preparation_index", 0)
        step_idx = attr.get("step_index", 0)
        recipe = attr.get("recipe", {"name": ""})
        name = recipe.get("name")
        preparations = recipe.get("preparation", [])

        if prep_idx < len(preparations):
            preparation = preparations[prep_idx]
            steps = preparation.get("steps",[])
            if step_idx +1 < len(steps):
                step_idx  +=1
                init = False
                ingredients = False
                preparation_state = False
                attr["init"] = init
                attr["ingredients"] =  ingredients
                attr["preparation"] = preparation_state
                attr["step_index"] = step_idx
            elif prep_idx+1 < len(preparations):
                prep_idx += 1
                step_idx = 0
                ingredients = True
                preparation_state = True
                attr["ingredients"] =  ingredients
                attr["preparation"] = preparation_state
                attr["step_index"] = step_idx
                attr["preparation_index"] = prep_idx
            else:
                speak = get_message(LANG_KEYS.skill_next_end_recipe)+"\n"
                handler_input.response_builder.speak(speak).set_card(
                    SimpleCard(name, speak)
                ).ask(speak)
                return handler_input.response_builder.response
            
        speech, display = SpeachRecipe.speach_recipe(
            recipe, prep_idx, step_idx, ingredients, init, preparation_state, step
        )
        handler_input.response_builder.speak(speech.speech).set_card(
            SimpleCard(name, display.speech)
        ).ask(speech.speech)
        return handler_input.response_builder.response
    
class PreviousIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        attr = handler_input.attributes_manager.session_attributes
        return is_intent_name("AMAZON.PreviousIntent")(handler_input) and attr.get("start", False) == True

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        attr = handler_input.attributes_manager.session_attributes
        
        init = attr.get("init", False)
        ingredients = attr.get("ingredients", False)
        preparation_state = attr.get("preparation", False)
        step = attr.get("step", False)
        prep_idx = attr.get("preparation_index", 0)
        step_idx = attr.get("step_index", 0)
        recipe = attr.get("recipe", {"name": ""})
        name = recipe.get("name")
        preparations = recipe.get("preparation", [])

        if prep_idx < len(preparations):
            preparation = preparations[prep_idx]
            steps = preparation.get("steps",[])
            if step_idx -1 >= 0:
                step_idx -=1
                attr["step_index"] = step_idx
                if step_idx == 0:
                    init = prep_idx == 0 
                    preparation_state = True
                    ingredients = True
                    attr["ingredients"] =  ingredients
                    attr["preparation"] = preparation_state
                    attr["init"] = init
                else:
                    init = False
                    attr["init"] = init

            elif prep_idx-1 >= 0:
                prep_idx -= 1
                preparation = preparations[prep_idx]
                steps = preparation.get("steps",[])
                step_idx = len(steps)-1
                ingredients = False
                preparation_state = False
                init = False
                attr["ingredients"] = ingredients
                attr["preparation"] = preparation_state
                attr["preparation_index"] = prep_idx
                attr["step_index"] = step_idx
                attr["init"] = init

            else:
                speak = get_message(LANG_KEYS.skill_prev_init_recipe)+"\n"
                handler_input.response_builder.speak(speak).set_card(
                    SimpleCard(name, speak)
                ).ask(speak)
                return handler_input.response_builder.response
            
        speech, display = SpeachRecipe.speach_recipe(
            recipe, prep_idx, step_idx, ingredients, init, preparation_state, step
        )
        handler_input.response_builder.speak(speech.speech).set_card(
            SimpleCard(name, display.speech)
        ).ask(speech.speech)
        return handler_input.response_builder.response



class CancelAndStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.CancelIntent")(handler_input) or is_intent_name(
            "AMAZON.StopIntent"
        )(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
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
        speech = get_message(LANG_KEYS.skill_exception)
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response
