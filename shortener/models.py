import random
import string

from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class ShortUrl(models.Model):
    # short_url could be pk as well
    URL_LENGTH = 6
    short_url = models.CharField(max_length=URL_LENGTH, blank=False, unique=True)
    long_url = models.URLField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    @classmethod
    def generate_short_url(cls) -> str:

        CHARACTERS = (
                string.ascii_uppercase
                + string.ascii_lowercase
                + string.digits
        )

        while True:
            short_url = ''.join(
                random.choice(CHARACTERS)
                for _ in range(cls.URL_LENGTH)
            )

            try:
                cls.objects.get(short_url=short_url)
            except ObjectDoesNotExist:
                return short_url

    def __str__(self):
        return f'<{self.long_url} to {self.short_url}>'
