from django.conf.urls import url
from django.contrib import admin
from Search import views

urlpatterns = [
    url(r'^search/', views.search),
    url(r'^select/', views.select),
]