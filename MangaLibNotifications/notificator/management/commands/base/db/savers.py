from .....models import User, Manga, MangaReading

from asgiref.sync import sync_to_async


async def user(ti, ui):
    u = User(ti, ui)
    await sync_to_async(u.save)()

    # Can use return to operate under the object after saving
    return u


async def manga(**data):
    m = Manga(**data)
    await sync_to_async(m.save)()

    return m


async def ref(u_obj, m_obj):
    await MangaReading.objects.aget_or_create(user_id=u_obj, manga_id=m_obj)
