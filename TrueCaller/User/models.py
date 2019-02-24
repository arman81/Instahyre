# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class User(models.Model):
	name = models.CharField(max_length = 100)
	email = models.CharField(max_length = 256)
	phonenumber = models.IntegerField()
	deviceId = models.CharField(max_length = 100)
	