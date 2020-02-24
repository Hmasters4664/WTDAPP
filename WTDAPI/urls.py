from django.conf.urls import url
from django.urls import include, re_path, path
from WTDAPI import views
from .views import GetProvinceEvents, Scrape, SearchEvents

urlpatterns = [
    path('register', views.create_user, name='register'),
    path('events', GetProvinceEvents.as_view(), name='get-events-province'),
    path('find', SearchEvents.as_view(),name='search'),
    path('reg', Scrape.as_view(), name='scrape'),
]