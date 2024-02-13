from django.urls import path
from shortener.views import ShortenUrl, GetOriginalUrl

urlpatterns = [
    path('<slug:short_url>', GetOriginalUrl.as_view(), name='get_original_url'),
    path('api/v1/shortener_urls/', ShortenUrl.as_view(), name='shorten_url'),
]
