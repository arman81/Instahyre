# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from User.models import User
from django.contrib.auth import views as auth_views
import json
from django.http import HttpResponse

def userinfo():
	if request.method ==  'POST'
	name = request.POST['name']
	email = request.POST['email']
	phonenumber = request.POST['phoneno']
	if(phonenumber=='' )
	try:
		user,created = User.objects.get_or_create(
			name=name,
			phonenumber=phonenumber,
			email=email,
			)
		if(created):
			return HttpResponse(json.dumps({'success':1,'message':'User created'}), content_type="application/json")
		else:
			return HttpResponse(json.dumps({'success':1,'message':'User edited'}), content_type="application/json")
	except Exception as e:
		raise e
