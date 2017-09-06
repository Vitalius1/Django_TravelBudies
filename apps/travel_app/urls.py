from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name = "index"),
    url(r'^logout$', views.logout, name = "logout"),
    url(r'^add$', views.add, name = "add"),
    url(r'^create_trip$', views.create_trip, name = "create_trip"),
    url(r'^join/(?P<trip_id>\d+)$', views.join, name = "join"),
    url(r'^tripInfo/(?P<trip_id>\d+)$', views.info, name = "tripInfo"),
]