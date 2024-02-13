from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ShortUrlModel
from .serializers import ShortUrlSerializer
from django.shortcuts import redirect


class ShortenUrl(APIView):

    def post(self, request):
        data = {
            'long_url': request.data.get('url'),
            'short_url': ShortUrlModel.generate_short_url(),
        }

        serializer = ShortUrlSerializer(data=data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)



