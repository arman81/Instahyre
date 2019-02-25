# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

#This is the global database
class Contacts(models.Model):
	name = models.CharField(db_index=True,max_length = 100,blank=True,null=True)
	email = models.CharField(max_length = 256,blank=True,null=True)
	phonenumber = models.IntegerField(db_index=True)
	deviceId = models.CharField(max_length = 100,blank=True,null=True)
	spam = models.BooleanField(default=False)
	no_of_spams_marked = models.PositiveIntegerField(default=0)
    