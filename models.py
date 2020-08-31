from django.db import models


class Api(models.Model):
    api_name = models.CharField(max_length=255)
    api_url = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255)
    api_value = models.CharField(max_length=255)
    access_token = models.CharField(max_length=255)
    token_count = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Api, on_delete=models.CASCADE)
    api_key = models.CharField(max_length=200)
    api_value = models.CharField(max_length=200)
    access_token = models.CharField(max_length=200)
    token_count = models.IntegerField(default=0)
