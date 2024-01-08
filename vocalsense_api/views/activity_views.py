from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from vocalsense_api.models import Activity
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import JSONParser
from vocalsense_api.serializers.activity_serializers import ActivitySerializer


class ActivityViewSet(viewsets.ModelViewSet):

    # Méthode pour recupérer la list des activites
    @action(detail=False, methods=['GET'])
    def list(self):
        queryset = Activity.objects.all()
        serializer = ActivitySerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    

    # Fonction permettant de faire  l'ajout d'une activité en base de donnée

    @action(detail=False, methods=['POST'])
    @csrf_exempt
    def store_activity(request):
        if request.method == 'POST':
            try:
                data = JSONParser().parse(request)
                nom_activite = data.get('nom_activite')
                campaign_id = data.get('campaign_id')

                # Vérifier si l\'activité avec le même nom existe déjà
                existing_activity = Activity.objects.filter(
                    nom_activite=nom_activite).first()

                if existing_activity:
                    return JsonResponse({'errorMessage': 'Une activité avec ce nom existe déjà.'}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')


                # Créer une nouvelle activite si elle n'existe pas
                activity = Activity.objects.create(nom_activite=nom_activite, campaign_id=campaign_id)


                # Après avoir enregistré l\'activité, mettre à jour la variable activity_list
                queryset = Activity.objects.all()
                activity_list = ActivitySerializer(queryset, many=True).data

              
                if activity:
                    return JsonResponse({
                        'successMessage': 'Activité enregistrée avec succès',
                        'activity_list': activity_list
                    },
                        status=status.HTTP_201_CREATED, content_type='application/json')


            except Exception as e:
                return JsonResponse({
                    'errorMessage': 'Erreur lors de la création de l\'activité : ' + str(e)},

                    status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type='application/json')

        else:
            return JsonResponse({'errorMessage': 'Méthode non autorisée'}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
        


    # Fonction permettant de faire la mise à jour d'une activité

    @action(detail=False, methods=['PUT'])
    @csrf_exempt
    def update_activity(request):
        if request.method == 'PUT':
            try:
                data = JSONParser().parse(request)
                nom_activite = data.get('nom_activite')
                activity_id = data.get('id')

                # Vérifier si l\'activité existe
                activity = Activity.objects.filter(id=activity_id).first()

                if not activity:
                    return JsonResponse({'errorMessage': 'L\'activité spécifiée n\'existe pas.'}, status=status.HTTP_404_NOT_FOUND, content_type='application/json')

                # Vérifier si une autre activite a déjà le même nom
                existing_activity = Activity.objects.exclude(
                    id=activity_id).filter(nom_activite=nom_activite).first()

                if existing_activity:
                    return JsonResponse({'errorMessage': 'Une activité avec ce nom existe déjà.'}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

                # Mettre à jour l\'activité
                activity.nom_activite = nom_activite
                activity.save()

                 # Après avoir enregistré l\'activité, mettre à jour la variable activity_list
                queryset = Activity.objects.all()
                activity_list = ActivitySerializer(queryset, many=True).data

                return JsonResponse({'successMessage': 'activite mise à jour avec succès',
                                     
                                     'activity_list': activity_list
                                     }, status=status.HTTP_200_OK, content_type='application/json')

            except Exception as e:
                return JsonResponse({'errorMessage': 'Erreur lors de la mise à jour de l\'activité : ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type='application/json')

        else:
            return JsonResponse({'errorMessage': 'Méthode non autorisée'}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
        
        

    # Fonction permettant de recupérer l\'activité à mettre à jours

    @action(detail=False, methods=['GET'])
    @csrf_exempt
    def get_activity(request, activity_id):
        if request.method == 'GET':
            try:
                # Vérifier si l\'activité existe
                activity = Activity.objects.filter(id=activity_id).first()

                if not activity:
                    return JsonResponse({'errorMessage': 'L\'activité spécifiée n\'existe pas.'}, status=status.HTTP_404_NOT_FOUND, content_type='application/json')

                # Récupérer les informations de l\'activité
                activity_data = {
                    'nom_activite': activity.nom_activite,
                    # Ajoutez d'autres champs au besoin
                }

                return JsonResponse(activity_data, status=status.HTTP_200_OK, content_type='application/json')

            except Exception as e:
                return JsonResponse({'errorMessage': 'Erreur lors de la récupération des informations de l\'activité : ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type='application/json')

        else:
            return JsonResponse({'errorMessage': 'Méthode non autorisée'}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

    # Fonction permettant de faire la suppression d'une activité

    @action(detail=True, methods=['DELETE'])
    @csrf_exempt
    def delete_activity(request, activity_id):
        if request.method == 'DELETE':
            try:
                # Vérifier si l\'activité existe
                activity = Activity.objects.filter(id=activity_id).first()

                if not activity:
                    return JsonResponse({'errorMessage': 'L\'activité spécifiée n\'existe pas.'}, status=status.HTTP_404_NOT_FOUND, content_type='application/json')

                # Supprimer l\'activité
                activity.delete()

                return JsonResponse({'successMessage': 'activite supprimée avec succès'}, status=status.HTTP_200_OK, content_type='application/json')

            except Exception as e:
                return JsonResponse({'errorMessage': 'Erreur lors de la suppression de l\'activité : ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type='application/json')
        else:
            return JsonResponse({'errorMessage': 'Méthode non autorisée'}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')