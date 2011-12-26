#-*- coding: utf-8 -*-

from django.db import models


class RequestToken(models.Model):
    key = models.CharField(max_length=255, unique=True)
    secret = models.CharField(max_length=255, unique=True)


class AccessToken(models.Model):
    userid = models.IntegerField(primary_key=True)
    key = models.CharField(max_length=255, unique=True)
    secret = models.CharField(max_length=255, unique=True)
