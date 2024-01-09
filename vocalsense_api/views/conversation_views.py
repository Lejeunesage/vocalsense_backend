from rest_framework import generics
from vocalsense_api.models import Conversation, Message
from vocalsense_api.serializers.message_serializers import MessageSerializer
from vocalsense_api.serializers.conversation_serializers import ConversationSerializer
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import JSONParser
import json
from datetime import datetime


class ConversationViewSet(viewsets.ModelViewSet):

    # Méthode pour recupérer la list des conversations
    @action(detail=False, methods=['GET'])
    def list(request):
        try:
            if request.method == 'GET':
                conversations = Conversation.objects.all()
                conversations_data = []

                for conversation in conversations:
                    messages = Message.objects.filter(conversation=conversation)
                    messages_data = []

                    for message in messages:
                        messages_data.append({
                            'expediteur': message.expediteur,
                            'contenu': message.contenu,
                            'heure_message': message.heure_conversation,
                        })

                    conversations_data.append({
                        'id': conversation.id,
                        'nom_teleconseiller': conversation.nom_teleconseiller,
                        'nom_client': conversation.nom_client,
                        'nom_superviseur': conversation.nom_superviseur,
                        'client_numero_telephone': conversation.client_numero_telephone,
                        'qualification_appel': conversation.qualification_appel,
                        'date_conversation': conversation.date_conversation,
                        'activity_id': conversation.activity_id,
                        'messages': messages_data,
                    })

                return JsonResponse({'conversations': conversations_data})

        except Exception as e:
            return JsonResponse({'error': f'Une erreur est survenue : {str(e)}'}, status=500)

        return JsonResponse({'message': 'Méthode non autorisée'}, status=405)
    
    

    # Fonction permettant de faire  l'ajout d'une conversation en base de donnée

    @action(detail=False, methods=['POST'])
    @csrf_exempt
    def store_conversation(request):
        try:
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))

                # Enregistrement de la conversation
                conversation = Conversation.objects.create(
                    nom_teleconseiller=data['conversation']['nom_teleconseiller'],
                    nom_client=data['conversation']['nom_client'],
                    nom_superviseur=data['conversation']['nom_superviseur'],
                    client_numero_telephone=data['conversation']['client_numero_telephone'],
                    qualification_appel=data['conversation']['qualification_appel'],
                    date_conversation=data['conversation']['date_conversation'],
                    activity_id=data['activity_id']
                )

                if conversation:

                    # Enregistrement des messages associés à la conversation
                    for message_data in data['conversation']['messages']:
                        Message.objects.create(
                            conversation=conversation,
                            expediteur=message_data['expediteur'],
                            contenu=message_data['contenu'],
                            heure_conversation=message_data['heure_message']
                )

                    return JsonResponse({'message': 'Conversation enregistrée avec succès!'})

        except Exception as e:
            return JsonResponse({'error': f'Une erreur est survenue : {str(e)}'}, status=500)

        return JsonResponse({'message': 'Méthode non autorisée'}, status=405)


    # Fonction permettant de faire la mise à jour d'une conversation

    @action(detail=False, methods=['PUT'])
    @csrf_exempt
    def update_conversation(request):
        if request.method == 'PUT':
            try:
                data = JSONParser().parse(request)
                nom_conversation = data.get('nom_conversation')
                conversation_id = data.get('id')

                # Vérifier si la conversation existe
                conversation = Conversation.objects.filter(id=conversation_id).first()

                if not conversation:
                    return JsonResponse({'errorMessage': 'la conversation spécifiée n\'existe pas.'}, status=status.HTTP_404_NOT_FOUND, content_type='application/json')

                # Vérifier si une autre conversation a déjà le même nom
                existing_conversation = Conversation.objects.exclude(
                    id=conversation_id).filter(nom_conversation=nom_conversation).first()

                if existing_conversation:
                    return JsonResponse({'errorMessage': 'Une conversation avec ce nom existe déjà.'}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

                # Mettre à jour la conversation
                conversation.nom_conversation = nom_conversation
                conversation.save()

                 # Après avoir enregistré la conversation, mettre à jour la variable conversation_list
                queryset = Conversation.objects.all()
                conversation_list = ConversationSerializer(queryset, many=True).data

                return JsonResponse({'successMessage': 'conversation mise à jour avec succès',
                                     
                                     'conversation_list': conversation_list
                                     }, status=status.HTTP_200_OK, content_type='application/json')

            except Exception as e:
                return JsonResponse({'errorMessage': 'Erreur lors de la mise à jour de la conversation : ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type='application/json')

        else:
            return JsonResponse({'errorMessage': 'Méthode non autorisée'}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
        
        

    # Fonction permettant de recupérer la conversation à mettre à jours

    @action(detail=False, methods=['GET'])
    @csrf_exempt
    def get_conversation(request, conversation_id):
        if request.method == 'GET':
            try:
                # Vérifier si la conversation existe
                conversation = Conversation.objects.filter(id=conversation_id).first()

                if not conversation:
                    return JsonResponse({'errorMessage': 'la conversation spécifiée n\'existe pas.'}, status=status.HTTP_404_NOT_FOUND, content_type='application/json')

                # Récupérer les informations de la conversation
                conversation_data = {
                    'nom_conversation': conversation.nom_conversation,
                    # Ajoutez d'autres champs au besoin
                }

                return JsonResponse(conversation_data, status=status.HTTP_200_OK, content_type='application/json')

            except Exception as e:
                return JsonResponse({'errorMessage': 'Erreur lors de la récupération des informations de la conversation : ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type='application/json')

        else:
            return JsonResponse({'errorMessage': 'Méthode non autorisée'}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

    # Fonction permettant de faire la suppression d'une conversation

    @action(detail=True, methods=['DELETE'])
    @csrf_exempt
    def delete_conversation(request, conversation_id):
        if request.method == 'DELETE':
            try:
                # Vérifier si la conversation existe
                conversation = Conversation.objects.filter(id=conversation_id).first()

                if not conversation:
                    return JsonResponse({'errorMessage': 'la conversation spécifiée n\'existe pas.'}, status=status.HTTP_404_NOT_FOUND, content_type='application/json')

                # Supprimer la conversation
                conversation.delete()

                return JsonResponse({'successMessage': 'conversation supprimée avec succès'}, status=status.HTTP_200_OK, content_type='application/json')

            except Exception as e:
                return JsonResponse({'errorMessage': 'Erreur lors de la suppression de la conversation : ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type='application/json')
        else:
            return JsonResponse({'errorMessage': 'Méthode non autorisée'}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
