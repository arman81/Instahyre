from django.conf.urls import url
from django.contrib import admin
from User import views
urlpatterns = [
    url(r'^user/', views.userinfo),
    url(r'^mark_spam/', views.mark_spam),
]
