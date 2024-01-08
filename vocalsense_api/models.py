from django.db import models

class Campaign(models.Model):
    nom_campagne = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.nom_campagne
    

class Activity(models.Model):
    nom_activite = models.CharField(max_length=255)
    campaign = models.ForeignKey('Campaign', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.nom_activite


class Keyword(models.Model):
    nom_motcle = models.CharField(max_length=255)
    activity = models.ForeignKey('Activity', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.nom_motcle


class Conversation(models.Model):
    nom_teleconseiller = models.CharField(max_length=255)
    nom_superviseur = models.CharField(max_length=255)
    nom_client = models.CharField(max_length=255)
    client_numero_telephone = models.CharField(max_length=20)
    qualification_appel = models.CharField(max_length=255)
    date_conversation = models.DateTimeField()
    activity = models.ForeignKey('Activity', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Conversation {self.id} - {self.nom_client}"


class Message(models.Model):
    contenu = models.TextField()
    expediteur = models.CharField(max_length=255)
    conversation = models.ForeignKey('Conversation', on_delete=models.CASCADE)
    heure_conversation = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Message {self.id} - {self.expediteur}"


class Statistic(models.Model):
    conversation = models.ForeignKey('Conversation', on_delete=models.CASCADE)
    keyword = models.ForeignKey('Keyword', on_delete=models.CASCADE)
    taux = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Statistic {self.id} - {self.keyword} - {self.taux}"
