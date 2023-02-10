from django.contrib import admin
from .models import Manga, User, MangaReading


admin.site.register(Manga)
admin.site.register(User)
admin.site.register(MangaReading)

