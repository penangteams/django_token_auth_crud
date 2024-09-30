from django.db import models
import os


class Profile(models.Model):
    def nameFile(instance, filename):
        return "/".join(["images", str(instance.name), filename])

    name = models.CharField(max_length=50)
    # Media file field
    media_file = models.FileField(upload_to=nameFile, blank=True, null=True)
