from typing import AnyStr
import requests
from app.core import configuration


class RecipesWebService:
    BASE_URL = configuration.APP_WS_RECIPES_URL
    SECRET = configuration.APP_WS_RECIPES_SECRET

    @classmethod
    def search_recipe(cls, search: str|None):
        headers = {"Authorization": f"Bearer {cls.SECRET}"}
        page_number = 0
        n_per_page = 5
        if search is None:
            # Get 1 Random
            n_per_page = 1
        params = dict(
            q=search,
            page_number=page_number,
            n_per_page=n_per_page
        )
        resp = requests.get(f"{cls.BASE_URL}/api/recipe/skill", headers=headers, params=params)
        if (resp.status_code == 200):
            data = resp.json()
            return data
        else:
            return None