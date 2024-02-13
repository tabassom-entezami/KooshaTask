import os
from typing import Dict

from django.conf import settings
from rest_framework import serializers
from shortener.models import ShortUrl


class ShortUrlField(serializers.Field):

    def to_representation(self, obj: 'ShortUrl'):
        """Deserializing"""
        return os.path.join(settings.SITE_URL, obj.short_url)

    def to_internal_value(self, short_url: str):

        if not short_url:
            raise serializers.ValidationError('Link is required!')
        if len(short_url) != ShortUrl.URL_LENGTH:
            raise serializers.ValidationError(
                f'Ensure this field has no more than {ShortUrl.URL_LENGTH} characters.'
            )

        return {'short_url': short_url}


class ShortUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortUrl
        fields = '__all__'
        read_only_fields = ['created_at', 'id']

    short_url = ShortUrlField(source='*')
    long_url = serializers.URLField(required=True)
    created_at = serializers.DateTimeField(read_only=True)
