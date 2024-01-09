from rest_framework import generics
from vocalsense_api.models import Keyword
from vocalsense_api.serializers.keyword_serializers import KeywordSerializer
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import JSONParser


class KeywordViewSet(viewsets.ModelViewSet):

    # Méthode pour recupérer la list des mots clés
    @action(detail=False, methods=['GET'])
    def list(self):
        queryset = Keyword.objects.all()
        serializer = KeywordSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    

    # Fonction permettant de faire  l'ajout d'un ou plusieurs mot(s) clé(s) en base de donnée

    @action(detail=False, methods=['POST'])
    @csrf_exempt
    def store_keyword(request):
        if request.method == 'POST':
            try:
                data = JSONParser().parse(request)
                nom_motcles = data.get('nom_motcles', [])
                activity_id = data.get('activity_id')

                # Vérifier si les mots clés avec les mêmes noms existent déjà
                existing_motcles = Keyword.objects.filter(
                    nom_motcle__in=nom_motcles).values_list('nom_motcle', flat=True)

                duplicate_motcles = set(existing_motcles)
                if duplicate_motcles:
                    return JsonResponse({
                        'errorMessage': f"Les mots clés suivants existent déjà : {', '.join(duplicate_motcles)}"
                    }, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

                # Créer de nouveaux mots clés
                keyword_list = []
                for nom_motcle in nom_motcles:
                    keyword = Keyword.objects.create(
                        nom_motcle=nom_motcle, activity_id=activity_id)
                    keyword_list.append(keyword)

                # Après avoir enregistré les mots clés, mettre à jour la variable keyword_list
                queryset = Keyword.objects.all()
                updated_keyword_list = KeywordSerializer(
                    queryset, many=True).data

                return JsonResponse({
                    'successMessage': 'Mots clés enregistrés avec succès',
                    'keyword_list': updated_keyword_list
                }, status=status.HTTP_201_CREATED, content_type='application/json')

            except Exception as e:
                return JsonResponse({
                    'errorMessage': f'Erreur lors de la création des mots clés : {str(e)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type='application/json')

        else:
            return JsonResponse({'errorMessage': 'Méthode non autorisée'}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
        


    # Fonction permettant de faire la mise à jour d'un mot clé

    @action(detail=False, methods=['PUT'])
    @csrf_exempt
    def update_keyword(request):
        if request.method == 'PUT':
            try:
                data = JSONParser().parse(request)
                nom_motcle = data.get('nom_motcle')
                keyword_id = data.get('id')

                # Vérifier si le mot clé existe
                keyword = Keyword.objects.filter(id=keyword_id).first()

                if not keyword:
                    return JsonResponse({'errorMessage': 'Le mot clé spécifié n\'existe pas.'}, status=status.HTTP_404_NOT_FOUND, content_type='application/json')

                # Vérifier si une autre activite a déjà le même nom
                existing_motcle = Keyword.objects.exclude(
                    id=keyword_id).filter(nom_motcle=nom_motcle).first()

                if existing_motcle:
                    return JsonResponse({'errorMessage': 'Un mot clé avec ce nom existe déjà.'}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

                # Mettre à jour le mot clé
                keyword.nom_motcle = nom_motcle
                keyword.save()

                 # Après avoir enregistré le mot clé, mettre à jour la variable keyword_list
                queryset = Keyword.objects.all()
                keyword_list = KeywordSerializer(queryset, many=True).data

                return JsonResponse({'successMessage': 'activite mise à jour avec succès',
                                     
                                     'keyword_list': keyword_list
                                     }, status=status.HTTP_200_OK, content_type='application/json')

            except Exception as e:
                return JsonResponse({'errorMessage': 'Erreur lors de la mise à jour de le mot clé : ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type='application/json')

        else:
            return JsonResponse({'errorMessage': 'Méthode non autorisée'}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
        
        

    # Fonction permettant de recupérer le mot clé à mettre à jours

    @action(detail=False, methods=['GET'])
    @csrf_exempt
    def get_keyword(request, keyword_id):
        if request.method == 'GET':
            try:
                # Vérifier si le mot clé existe
                keyword = Keyword.objects.filter(id=keyword_id).first()

                if not keyword:
                    return JsonResponse({'errorMessage': 'Le mot clé spécifié n\'existe pas.'}, status=status.HTTP_404_NOT_FOUND, content_type='application/json')

                # Récupérer les informations de le mot clé
                keyword_data = {
                    'nom_motcle': keyword.nom_motcle,
                    # Ajoutez d'autres champs au besoin
                }

                return JsonResponse(keyword_data, status=status.HTTP_200_OK, content_type='application/json')

            except Exception as e:
                return JsonResponse({'errorMessage': 'Erreur lors de la récupération des informations de le mot clé : ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type='application/json')

        else:
            return JsonResponse({'errorMessage': 'Méthode non autorisée'}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

    # Fonction permettant de faire la suppression d'un mot clé

    @action(detail=True, methods=['DELETE'])
    @csrf_exempt
    def delete_keyword(request, keyword_id):
        if request.method == 'DELETE':
            try:
                # Vérifier si le mot clé existe
                keyword = Keyword.objects.filter(id=keyword_id).first()

                if not keyword:
                    return JsonResponse({'errorMessage': 'Le mot clé spécifié n\'existe pas.'}, status=status.HTTP_404_NOT_FOUND, content_type='application/json')

                # Supprimer le mot clé
                keyword.delete()

                return JsonResponse({'successMessage': 'activite supprimée avec succès'}, status=status.HTTP_200_OK, content_type='application/json')

            except Exception as e:
                return JsonResponse({'errorMessage': 'Erreur lors de la suppression de le mot clé : ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type='application/json')
        else:
            return JsonResponse({'errorMessage': 'Méthode non autorisée'}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')