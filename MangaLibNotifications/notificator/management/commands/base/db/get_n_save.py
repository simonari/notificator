from django.core.files import File
from django.core.files.base import ContentFile

import requests
import json

from .....models import Manga

from asgiref.sync import sync_to_async

from . import savers
from .getters import bulk

base_url = "https://mangalib.me"


async def cover_img(salt, cover):
    url = "https://cover.imglib.info/uploads/cover"
    url = f"{url}/{salt}/cover/{cover}_250x350.jpg"

    response = requests.get(url)

    img = File(ContentFile(response.content), f"{salt}.jpg")

    return img


async def manga_data(user):
    url = f"{base_url}/bookmark/{user.pi}"
    response = requests.get(url)
    content = response.content

    manga_list = json.loads(content)['items']
    manga_ids = await sync_to_async(list)(await bulk.mis())

    for i, item in enumerate(manga_list):
        if item["manga_id"] in manga_ids:
            print(f"Manga with id: {item['manga_id']} already exists in database")
            continue

        data = {
            "mi": item["manga_id"],
            "name_eng": item["manga_name"],
            "name_ru": item["rus_name"],
            "last_ch": item["last_chapter"]["number"],
            # TODO use timezoned timestamp instead of naive format
            "last_ch_time": item["last_chapter_at"],
            "last_volume": item["last_chapter"]["volume"],
            "salt": item["slug"],
            "cover_img": await cover_img(item["slug"], item["cover"])
        }

        # Saving manga and reference between user and manga
        manga = await savers.manga(**data)
        await savers.ref(user, manga)