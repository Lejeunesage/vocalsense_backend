from rest_framework import serializers
from vocalsense_api.models import Keyword

class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = '__all__'
