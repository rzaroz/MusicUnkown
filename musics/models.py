from django.db import models


class Musics(models.Model):
    username = models.CharField(max_length=20, verbose_name="User name")
    music_name = models.CharField(max_length=20, verbose_name="Music name")
    music = models.FileField(verbose_name="Music", upload_to="Musics")

    def __str__(self):
        return self.music_name