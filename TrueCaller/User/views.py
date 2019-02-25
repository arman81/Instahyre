# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.shortcuts import render
from User.models import User
from Search.models import Contacts
from django.contrib.auth import views as auth_views
import json
from django.http import HttpResponse
import re
import redis
#connecting with redis
REDIS = redis.StrictRedis(host='localhost', port=6379, db=0)

@login_required
def userinfo():
	if request.method ==  'POST':			
		name = request.POST['name']
		email = request.POST['email']
		phonenumber = request.POST['phonenumber']
		valid = validate_number(phonenumber)
		if(not valid):
			return HttpResponse(json.dumps({'success':0,'error':400,'message':'Invalid phone number'}), content_type="application/json")
		if(phonenumber=='' or not phonenumber or name=='' or not name):
			return HttpResponse(json.dumps({'success':0,'error':400,'message':'Mandatory Parameters missing'}), content_type="application/json")
		try:
			#Personal DB update
			user,created = User.objects.using('users').get_or_create(
				name=name,
				phonenumber=phonenumber,
				email=email
				)
			#Global DB update	
			Contacts.objects.create(
				name=name,
				phonenumber=phonenumber,
				email=email
			)
			set_redis(phonenumber,json.dumps(user))  #Hooks for populating redis by phonenumber
			set_redis(name,json.dumps(user))         #Hooks for populating redis by name
			if(created):
				return HttpResponse(json.dumps({'success':1,'message':'User created'}), content_type="application/json")
			else:
				return HttpResponse(json.dumps({'success':1,'message':'User edited'}), content_type="application/json")
		except Exception as e:
			return HttpResponse(json.dumps({'success':1,'error':500,'message':str(e)}), content_type="application/json")
	else:
		u = User.objects.get(request.GET['id'])
		return HttpResponse(json.dumps({user:u,'sucess':1}), content_type="application/json")		


@login_required
def mark_spam(request):
	try:
		id = request['phonenumber']
		user = Contacts.objects.get_or_create(phonenumber=phonenumber) #handles the case if the number is already registered or not
		if(not user):
			return HttpResponse(json.dumps({'success':0,'error':404,'message':'No user found'}), content_type="application/json")
		user.spam = True
		user.no_of_spam_marked = user.no_of_spam_marked + 1
		set_redis(user.phonenumber,user)
		set_redis(user.name,user)
		user.save()
		return HttpResponse(json.dumps({'success':1}), content_type="application/json")
	except Exception as e:
		return HttpResponse(json.dumps({'success':0,'error':500,'message':str(e)}), content_type="application/json")


def validate_number(value):
    rule = re.compile(r'(^[+0-9]{1,3})*([0-9]{10,11}$)')
    if rule.search(value):
        return True
    else:
        return False

def set_redis(key, value):
    try:
        REDIS.set(key,  json.dumps(value))
        return True
    except Exception as e:
        print("Error in setting " + key + "to " + str(value) + str(e))
        return False



