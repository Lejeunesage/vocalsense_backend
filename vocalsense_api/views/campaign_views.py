from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from vocalsense_api.models import Campaign
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import JSONParser
from vocalsense_api.serializers.campaign_serializers import CampaignSerializer


class CampagnViewSet(viewsets.ModelViewSet):

    # Méthode pour recupérer la list des campagnes
    @action(detail=False, methods=['GET'])
    def list(self):
        queryset = Campaign.objects.all()
        serializer = CampaignSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    

    # Fonction permettant de faire  l'ajout d'une campagne en base de donnée

    @action(detail=False, methods=['POST'])
    @csrf_exempt
    def store_campaign(request):
        if request.method == 'POST':
            try:
                data = JSONParser().parse(request)
                nom_campagne = data.get('nom_campagne')

                # Vérifier si la campagne avec le même nom existe déjà
                existing_campaign = Campaign.objects.filter(
                    nom_campagne=nom_campagne).first()

                if existing_campaign:
                    return JsonResponse({'errorMessage': 'Une campagne avec ce nom existe déjà.'}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')


                # Créer une nouvelle campagne si elle n'existe pas
                campaign = Campaign.objects.create(nom_campagne=nom_campagne)


                # Après avoir enregistré la campagne, mettre à jour la variable campaign_list
                queryset = Campaign.objects.all()
                campaign_list = CampaignSerializer(queryset, many=True).data

              
                if campaign:
                    return JsonResponse({
                        'successMessage': 'Campagne enregistrée avec succès',
                        'campaign_list': campaign_list
                    },
                        status=status.HTTP_201_CREATED, content_type='application/json')


            except Exception as e:
                return JsonResponse({
                    'errorMessage': 'Erreur lors de la création de la campagne : ' + str(e)},

                    status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type='application/json')

        else:
            return JsonResponse({'errorMessage': 'Méthode non autorisée'}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
        


    # Fonction permettant de faire la mise à jour d'une campagne

    @action(detail=False, methods=['PUT'])
    @csrf_exempt
    def update_campaign(request):
        if request.method == 'PUT':
            try:
                data = JSONParser().parse(request)
                nom_campagne = data.get('nom_campagne')
                campaign_id = data.get('id')

                # Vérifier si la campagne existe
                campaign = Campaign.objects.filter(id=campaign_id).first()

                if not campaign:
                    return JsonResponse({'errorMessage': 'La campagne spécifiée n\'existe pas.'}, status=status.HTTP_404_NOT_FOUND, content_type='application/json')

                # Vérifier si une autre campagne a déjà le même nom
                existing_campaign = Campaign.objects.exclude(
                    id=campaign_id).filter(nom_campagne=nom_campagne).first()

                if existing_campaign:
                    return JsonResponse({'errorMessage': 'Une campagne avec ce nom existe déjà.'}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

                # Mettre à jour la campagne
                campaign.nom_campagne = nom_campagne
                campaign.save()

                 # Après avoir enregistré la campagne, mettre à jour la variable campaign_list
                queryset = Campaign.objects.all()
                campaign_list = CampaignSerializer(queryset, many=True).data

                return JsonResponse({'successMessage': 'Campagne mise à jour avec succès',
                                     
                                     'campaign_list': campaign_list
                                     }, status=status.HTTP_200_OK, content_type='application/json')

            except Exception as e:
                return JsonResponse({'errorMessage': 'Erreur lors de la mise à jour de la campagne : ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type='application/json')

        else:
            return JsonResponse({'errorMessage': 'Méthode non autorisée'}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
        
        

    # Fonction permettant de recupérer la campagne à mettre à jours

    @action(detail=False, methods=['GET'])
    @csrf_exempt
    def get_campaign(request, campaign_id):
        if request.method == 'GET':
            try:
                # Vérifier si la campagne existe
                campaign = Campaign.objects.filter(id=campaign_id).first()

                if not campaign:
                    return JsonResponse({'errorMessage': 'La campagne spécifiée n\'existe pas.'}, status=status.HTTP_404_NOT_FOUND, content_type='application/json')

                # Récupérer les informations de la campagne
                campaign_data = {
                    'nom_campagne': campaign.nom_campagne,
                    # Ajoutez d'autres champs au besoin
                }

                return JsonResponse(campaign_data, status=status.HTTP_200_OK, content_type='application/json')

            except Exception as e:
                return JsonResponse({'errorMessage': 'Erreur lors de la récupération des informations de la campagne : ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type='application/json')

        else:
            return JsonResponse({'errorMessage': 'Méthode non autorisée'}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

    # Fonction permettant de faire la suppression d'une campagne

    @action(detail=True, methods=['DELETE'])
    @csrf_exempt
    def delete_campaign(request, campaign_id):
        if request.method == 'DELETE':
            try:
                # Vérifier si la campagne existe
                campaign = Campaign.objects.filter(id=campaign_id).first()

                if not campaign:
                    return JsonResponse({'errorMessage': 'La campagne spécifiée n\'existe pas.'}, status=status.HTTP_404_NOT_FOUND, content_type='application/json')

                # Supprimer la campagne
                campaign.delete()

                return JsonResponse({'successMessage': 'Campagne supprimée avec succès'}, status=status.HTTP_200_OK, content_type='application/json')

            except Exception as e:
                return JsonResponse({'errorMessage': 'Erreur lors de la suppression de la campagne : ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type='application/json')
        else:
            return JsonResponse({'errorMessage': 'Méthode non autorisée'}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')