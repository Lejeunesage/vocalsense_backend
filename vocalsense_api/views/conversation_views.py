from rest_framework import generics
from vocalsense_api.models import Conversation
from vocalsense_api.serializers.conversation_serializers import ConversationSerializer

class ConversationList(generics.ListCreateAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

class ConversationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
