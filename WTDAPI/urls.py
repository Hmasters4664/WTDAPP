from django.conf.urls import url
from django.urls import include, re_path, path
from WTDAPI import views

urlpatterns = [
    path('register', views.create_user, name='register'),
]