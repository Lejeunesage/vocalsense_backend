from rest_framework import generics
from vocalsense_api.models import Keyword
from vocalsense_api.serializers.keyword_serializers import KeywordSerializer

class KeywordList(generics.ListCreateAPIView):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer

class KeywordDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer
