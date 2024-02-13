from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ShortUrl
from .serializers import ShortUrlSerializer
from django.shortcuts import redirect
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django.core.cache import caches,cache

''' ViewSet instead of APIVIEW would take less work but I can also set the throttling policy on
 a per-view or per-viewset basis, using the APIView class-based views.'''


class ShortenUrl(APIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def post(self, request):
        data = {
            'long_url': request.data.get('url'),
            'short_url': ShortUrl.generate_short_url(),
        }

        self.serializer = ShortUrlSerializer(data=data)
        serializer = self.serializer
        serializer.is_valid(raise_exception=True)
        serializer.save()
        cache.set(serializer.short_url, serializer.long_url, 300)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Q does spiliting the request add help to find ip?

class GetOriginalUrl(APIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get(self, request, short_url: str):

        if cache.get(short_url):
            return redirect(cache.get(short_url))
        try:
            obj = ShortUrl.objects.all().get(short_url=short_url)

        except request.ObjectDoesNotExist:
            return Response({'error': 'Short url id does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        cache.set(short_url, obj.long_url, 300)
        return redirect(obj.long_url)
