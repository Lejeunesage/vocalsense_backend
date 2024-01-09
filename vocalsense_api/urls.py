# vocalsense_api/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views.campaign_views import CampagnViewSet
from .views.activity_views import ActivityViewSet
from .views.keyword_views import KeywordViewSet
from .views.conversation_views import ConversationList, ConversationDetail
from .views.message_views import MessageList, MessageDetail
from .views.statistic_views import StatisticList, StatisticDetail

router = DefaultRouter()
router.register(r'campaigns', CampagnViewSet, basename='campaigns')

urlpatterns = [
    # Les URLs pour les opérations CRUD Campagne
    path('campaigns-list', CampagnViewSet.list, name='campaigns-list'),
    path('store-campaign', CampagnViewSet.store_campaign, name='store-campaign'),
    path('update-campaign', CampagnViewSet.update_campaign, name='update-campaign'),
    path('<int:campaign_id>/get-campaign', CampagnViewSet.get_campaign, name='get-campaign-detail'),
    path('<int:campaign_id>/delete-campaign', CampagnViewSet.delete_campaign, name='campaign-delete'),

    # Les URLs pour les opérations CRUD Activité
    path('activities-list', ActivityViewSet.list, name='activities-list'),
    path('store-activity', ActivityViewSet.store_activity, name='store-activity'),
    path('update-activity', ActivityViewSet.update_activity, name='update-activity'),
    path('<int:activity_id>/get-activity', ActivityViewSet.get_activity, name='get-activity-detail'),
    path('<int:activity_id>/delete-activity', ActivityViewSet.delete_activity, name='activity-delete'),

    # Les URLs pour les opérations CRUD Mot Clé
    path('keywords-list', KeywordViewSet.list, name='Keywords-list'),
    path('store-keyword', KeywordViewSet.store_keyword, name='store-keyword'),
    path('update-keyword', KeywordViewSet.update_keyword, name='update-keyword'),
    path('<int:keyword_id>/get-keyword', KeywordViewSet.get_keyword, name='get-keyword-detail'),
    path('<int:keyword_id>/delete-keyword', KeywordViewSet.delete_keyword, name='keyword-delete'),
    
   
    

    path('conversations/', ConversationList.as_view(), name='conversation-list'),
    path('conversations/<int:pk>/', ConversationDetail.as_view(), name='conversation-detail'),

    path('messages/', MessageList.as_view(), name='message-list'),
    path('messages/<int:pk>/', MessageDetail.as_view(), name='message-detail'),

    path('statistics/', StatisticList.as_view(), name='statistic-list'),
    path('statistics/<int:pk>/', StatisticDetail.as_view(), name='statistic-detail'),
]
