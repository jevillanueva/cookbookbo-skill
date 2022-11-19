import json
from fastapi import APIRouter, Request, status
from app.core.configuration import APP_ALEXA_SKILL_ID
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_webservice_support.webservice_handler import WebserviceSkillHandler
from app.alexa import default_intents, cookbookbo
router = APIRouter()
skill_builder = SkillBuilder()
skill_builder.skill_id  = APP_ALEXA_SKILL_ID  # type: ignore
# Default Intents
skill_builder.add_request_handler(default_intents.LaunchRequestHandler())
skill_builder.add_request_handler(default_intents.HelpIntentHandler())
skill_builder.add_request_handler(default_intents.CancelAndStopIntentHandler())
skill_builder.add_request_handler(default_intents.SessionEndedRequestHandler())
skill_builder.add_exception_handler(default_intents.AllExceptionHandler())
# Own Intents
skill_builder.add_request_handler(cookbookbo.GetRecipeIntentHandler())
webservice_handler = WebserviceSkillHandler(skill=skill_builder.create())

@router.post("/cookbookbo", status_code=status.HTTP_200_OK)
async def endpoint(req: Request):
    data = await req.body()
    datajson = data.decode("utf-8")
    response = webservice_handler.verify_request_and_dispatch(req.headers, datajson)  # type: ignore
    return json.dumps(response)