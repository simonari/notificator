from ......models import User, Manga, MangaReading

from . import objects


async def manga_cover(mi):
    return (await objects.manga_obj(mi)).cover_img


async def user_pi(ti):
    return (await objects.user_obj(ti)).pi
