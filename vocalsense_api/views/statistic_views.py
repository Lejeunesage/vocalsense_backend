from rest_framework import generics
from vocalsense_api.models import Statistic
from vocalsense_api.serializers.statistic_serializers import StatisticSerializer

class StatisticList(generics.ListCreateAPIView):
    queryset = Statistic.objects.all()
    serializer_class = StatisticSerializer

class StatisticDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Statistic.objects.all()
    serializer_class = StatisticSerializer
