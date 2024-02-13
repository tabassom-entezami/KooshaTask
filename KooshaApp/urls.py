from django.urls import path
from KooshaApp.views import ShortenUrl, GetOriginalUrl

urlpatterns = [
    path('<str:short_url>', GetOriginalUrl.as_view(), name='get_original_url'),
    path('shorten-url/', ShortenUrl.as_view(), name='shorten_url'),
]
