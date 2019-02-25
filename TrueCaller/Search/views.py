# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django import db
from threading import Thread
import pymongo
import json
from multiprocessing import Pool
from django.conf import settings
import redis
from Search.models import Contacts
import json
from django.http import HttpResponse
import redis
from itertools import chain
#connecting with redis
REDIS = redis.StrictRedis(host='localhost', port=6379, db=0)
import re

#@login_required
def search(request):
	if request.method == 'GET':
		keyword = request.GET['keyword']
		pool = Pool(processes=2)
		Personal = pool.apply_async(search_personal,[user.id],[keyword])
		Global = pool.apply_async(search_global,user.id)
		pool.close()
		pool.join()                
		final_results = chain(Personal.get(),Global.get())
		return HttpResponse(json.dumps({'success':1,'result':result}), content_type="application/json") 
	else:
		return HttpResponse(json.dumps({'success':0,'message':'Bad Request'}))	

def search_personal(user_id,keyword):
	results = []
	try:
		personal_contacts = User.objects.using('users').filter(id=user_id)
		for contact in personal_contacts:
			pattern = re.compile(contact.name)
			if(pattern.match(keyword)):
				results.append(contact)
		return results
	except Exception as e:
		print('Error '+str(e))
		return results


def search_global(keyword):
	results = []
	try:
		for key in REDIS.keys('*keyword*'):
			results.append(redis.get(key))
		return results
	except Exception as e:
		print('Error '+str(e))
		return results
	


@login_required
def select(request):
	if request.method == 'GET':
		try:
			id = request.GET['id']
			contact = Contacts.objects.filter(id=id)
			return HttpResponse(json.dumps({'success':1,'contact':contact}), content_type="application/json")
		except Exception as e:
			return HttpResponse(json.dumps({'success':0,'message':str(e),'error':500}), content_type="application/json")
			

		

