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
        # Or using Viewset
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GetOriginalUrl(APIView):

    def get(self, request, short_url: str):
        try:
            obj = ShortUrlModel.objects.all().get(short_url=short_url)

        except request.ObjectDoesNotExist:
            return Response({'error': 'Short url id does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        ShortUrlSerializer(obj)
        return redirect(obj.long_url)
        # return Response(serializer.data, status=status.HTTP_200_OK)
