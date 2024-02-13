from django.contrib import admin

from shortener.models import ShortUrl


@admin.register(ShortUrl)
class ShortUrlAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_url', 'long_url', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('long_url',)
    ordering = ('-created_at',)
    list_display_links = ('id', 'short_url')
    list_per_page = 20

