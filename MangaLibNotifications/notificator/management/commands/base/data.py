import requests
from bs4 import BeautifulSoup as bs
import re
import json
from .db.getters import objects

async def get_manga_data(mi):
    manga = await objects.manga_obj(mi)
    url = f"https://mangalib.me/{manga.salt}?section=chapters"

    response = requests.get(url)

    if response.status_code != 200:
        return None

    soup = bs(response.content, "html.parser")

    pattern = re.compile("window.__DATA__ = (.+?);")
    script = soup.find("script", string=pattern)

    data = re.findall(pattern, script.string)[0]
    last_update = json.loads(data)["chapters"]["list"][0]["chapter_created_at"]

    return last_update, response