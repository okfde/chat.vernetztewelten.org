from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('enter/', views.enter_room, name='enter-room'),
    url(r'^room/(?P<room_uuid>[^/]+)/$', views.room, name='room'),
]
