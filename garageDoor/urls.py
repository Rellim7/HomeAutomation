from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^open/$', views.openDoor, name='open'),
    url(r'^close/$', views.closeDoor, name='close'),
    url(r'^forceclose/$', views.forceCloseDoor, name='FORCE CLOSING'),
    url(r'^status/$', views.statusCheck, name='open'),
]
