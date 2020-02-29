from django.conf.urls import url
from django.urls import include, re_path, path
from WTDAPI import views
from .views import GetProvinceEvents, Scrape, SearchEvents, GetProvinceDateEvents, GetProvinceCategoryEvents, SearchAll\
    , GetEvents


urlpatterns = [
    path('register', views.create_user, name='register'),
    path('events', GetEvents.as_view(), name='get-events-province'),
    path('find', SearchEvents.as_view(),name='search'),
    path('reg', Scrape.as_view(), name='scrape'),
    path('searchdate', GetProvinceDateEvents.as_view(), name='search-date'),
    path('searchcategory', GetProvinceCategoryEvents.as_view(), name='search-category'),
    path('search', SearchAll.as_view(), name='search'),
]