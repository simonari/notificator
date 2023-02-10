from django.db import models


class BaseModel(models.Model):
    objects = models.Manager

    class Meta:
        abstract = True


class User(BaseModel):
    """
    User class defined to store data about user
    Fields:
        ti: telegram id of chat
        pi: MangaLib id of profile
    """
    ti = models.PositiveIntegerField(
        primary_key=True,
        verbose_name="Telegram ID"
    )
    pi = models.PositiveIntegerField(
        verbose_name="Profile ID"
    )

    def __str__(self):
        return f"User #{self.ti}"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class Manga(BaseModel):
    """
    Manga class defined to store data about manga
    """
    mi = models.PositiveIntegerField(
        primary_key=True,
        verbose_name="Manga ID"
    )
    name_eng = models.CharField(
        max_length=50,
        verbose_name="Manga title (ENG)"
    )
    name_ru = models.CharField(
        max_length=50,
        verbose_name="Manga title (RU)"
    )
    last_ch = models.FloatField(
        verbose_name="Last chapter"
    )
    last_ch_time = models.DateTimeField(
        default=None,
        verbose_name="Last chapter release time"
    )
    last_volume = models.PositiveIntegerField(
        verbose_name="Last volume"
    )
    # TODO
    #   Rename "salt" -> "slug"
    salt = models.CharField(max_length=50)
    cover = models.CharField(
        max_length=16,
        verbose_name="Cover slug"
    )
    # TODO
    #   Choose another directory
    cover_img = models.ImageField(
        upload_to="images/",
        verbose_name="Cover image"
    )


    def __str__(self):
        return self.name_eng


    class Meta:
        verbose_name = "Manga"
        verbose_name_plural = "Manga list"


class MangaReading(BaseModel):
    """
    MangaReading class defined to create relationship between User and Manga classes
    """
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    manga_id = models.ForeignKey(Manga, to_field='mi', on_delete=models.CASCADE)


    def __str__(self):
        return f"#{self.user_id.ti}"


    class Meta:
        verbose_name = "Readable manga"
        verbose_name_plural = "Readable manga list"
