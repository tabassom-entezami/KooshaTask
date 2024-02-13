from django.contrib import admin

from KooshaApp.models import ShortUrlModel


@admin.register(ShortUrlModel)
class ShortUrlAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_url', 'long_url', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('long_url',)
    ordering = ('-created_at',)

