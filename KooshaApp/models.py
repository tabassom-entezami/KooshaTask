import random
import string

from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class ShortUrlModel(models.Model):
    URL_LENGTH = 6
    short_url = models.CharField(max_length=URL_LENGTH, blank=False, unique=True)
    long_url = models.URLField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    @classmethod
    def generate_short_id(cls) -> str:

        CHARACTERS = (
                string.ascii_uppercase
                + string.ascii_lowercase
                + string.digits
        )

        while True:
            short_id = ''.join(
                random.choice(CHARACTERS)
                for _ in range(cls.ID_LENGTH)
            )

            try:
                cls.objects.get(short_id=short_id)
            except ObjectDoesNotExist:
                return short_id

    def get_absolute_url(self):
        return reverse('redirect', kwargs={'short_url': self.short_url})

    def __str__(self):
        return f'{self.long_url} to {self.short_url}'
