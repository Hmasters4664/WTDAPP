from django.conf.urls import url
from django.urls import include, re_path, path
from WTDAPI import views
from .views import GetProvinceEvents, Scrape

urlpatterns = [
    path('register', views.create_user, name='register'),
    re_path('events/(?P<province>[\w-]+)/$', GetProvinceEvents.as_view(), name='get-events-province'),
    path('reg', Scrape.as_view(), name='scrape'),
]