from ......models import User, Manga, MangaReading

from asgiref.sync import sync_to_async


@sync_to_async
def mis_ref(ti):
    return MangaReading.objects \
        .filter(user_id=ti) \
        .values_list("manga_id", flat=True)


@sync_to_async
def mis():
    return Manga.objects\
        .values_list("mi", flat=True)