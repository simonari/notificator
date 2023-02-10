from ......models import User, Manga, MangaReading

from asgiref.sync import sync_to_async


async def manga_obj(mi):
    return await Manga.objects.aget(pk=mi)


async def manga_ref(ti):
    # returns QuerySet contains references between user with given ti and it's mangas
    return await sync_to_async(MangaReading.objects.filter)(user_id=ti)


async def user_obj(ui):
    return await User.objects.aget(pk=ui)
