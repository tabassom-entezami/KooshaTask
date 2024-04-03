import random
import string

from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

class Plan(models.Model):
    title = models.TextField(max_length=255, blank=True, null=True)
    description = models.TextField(max_length=255, blank=True, null=True)
    limited_create_number = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1)])
    duration_day = models.IntegerField(default=90, blank=True, validators=[MinValueValidator(1)])
    max_length = models.IntegerField(default=8, validators=[MinValueValidator(1)])
    min_length = models.IntegerField(default=6, validators=[MinValueValidator(1)])
    extera_back_half_allowed = models.BooleanField(default=True, blank=True)
    back_half_allowed = models.BooleanField(default=True, blank=True)
    lower_case_characters = models.BooleanField(default=True, blank=True)
    number_characters = models.BooleanField(default=True, blank=True)
    upper_case_characters = models.BooleanField(default=True, blank=True)
    other_characters = models.BooleanField(default=True, blank=True)
    eternal_allowed = models.BooleanField(default=False, blank=True)
    price = models.IntegerField(blank=True, null=True, default=None)
    has_advertise_plan = models.BooleanField(default=False, blank=True)
    has_sms_plan = models.BooleanField(default=False, blank=True)
    is_active = models.BooleanField(default=True, blank=True)
    datetime_created = models.DateTimeField(auto_now_add=True, blank=True)

    #todo validate price
    def save(self, *args, **kwargs):
        if self.max_length >= self.min_length:
            return super(Plan, self).save(*args, **kwargs)
        max_len = max(self.max_length, self.min_length)
        min_len = min(self.min_length, self.max_length)
        self.max_length = max_len
        self.min_length = min_len
        return super(Plan, self).save(*args, **kwargs)

class ShortUrl(models.Model):
    # short_url could be pk as well
    URL_LENGTH = 6
    short_url = models.CharField(max_length=URL_LENGTH, blank=False, unique=True)
    long_url = models.URLField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    # def get_usage_data(self):
    #     CHARACTERS = ''
    #     if self.user_plan.plan.lower_case_characters:
    #         CHARACTERS += string.ascii_lowercase.replace('i', '').replace('o', '').replace('l', '')
    #     if self.user_plan.plan.upper_case_characters:
    #         CHARACTERS += string.ascii_uppercase.replace('I', '').replace('O', '').replace('L', '')
    #     if self.user_plan.plan.other_characters:
    #         CHARACTERS += r"""!&()*+-.:;=?@_"""
    #     if self.user_plan.plan.number_characters:
    #         CHARACTERS += string.digits.replace('0', '').replace('1', '')
    #
    #     limited_create_number = self.user_plan.plan.limited_create_number
    #     eternal_allowed = self.user_plan.plan.eternal_allowed
    #     max_length = self.user_plan.plan.max_length
    #     min_length = self.user_plan.plan.min_length
    #     back_half_allowed = self.user_plan.plan.back_half_allowed
    #     extera_back_half_allowed = self.user_plan.plan.extera_back_half_allowed
    #
    #     data = {'CHARACTERS': CHARACTERS, 'limited_create_number': limited_create_number,
    #             'eternal_allowed': eternal_allowed, 'max_length': max_length, 'min_length': min_length,
    #             'back_half_allowed': back_half_allowed, 'extera_back_half_allowed': extera_back_half_allowed, }
    #     return data

    # def set_domain(self):
    #     schemes = ["http", "https", "ftp", "ftps"]
    #     unsafe_chars = frozenset("\t\r\n")
    #
    #     if not isinstance(self.long_url, str) or unsafe_chars.intersection(self.long_url):
    #         return None
    #
    #     try:
    #         splitted_url = urlsplit(self.long_url)
    #         unsplit_scheme = self.long_url.split("://")[0].lower()
    #         if splitted_url.hostname is None or len(splitted_url.hostname) > 253 or unsplit_scheme not in schemes:
    #             return None
    #         scheme, netloc, path, query, fragment = splitted_url
    #         return netloc
    #     except 'not a valid URL':
    #         return None

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
