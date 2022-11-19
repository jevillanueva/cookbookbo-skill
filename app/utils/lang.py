from enum import Enum
import os
import traceback
import yaml


from app.core import configuration

LANG = configuration.APP_LANG
dirpath = os.path.dirname(__file__)
path = os.path.join(dirpath, "..", "lang", LANG + ".yaml")
dictionary = dict()
with open(path, encoding="utf-8") as fh:
    try:
        dictionary = yaml.safe_load(fh)
    except yaml.YAMLError as exc:
        print(exc)

class LANG_KEYS(Enum):
    default = "default"
    title = "title"
    skill_hello = "skill_hello"
    skill_help = "skill_help"
    skill_cancel = "skill_cancel"
    skill_exception = "skill_exception"

def get_message(key:LANG_KEYS):
    if not isinstance(key,LANG_KEYS):
        raise TypeError('direction must be an instance of Direction Enum')
    try:
        message = dictionary[key.value]
        return message
    except:
        try:
            traceback.print_exc()
            return dictionary[LANG_KEYS.default]
        except:
            traceback.print_exc()
            return 'Something went wrong with the dictionary "{0}"'.format(LANG)