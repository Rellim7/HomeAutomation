from django.shortcuts import render
from django.http import HttpResponse
from garageDoor.models import door, openEvent, closeEvent
from services import controller
# Create your views here.
def index(request):
    return Httpresponse("Welcome To Prime Ingenuitys Garage door division")

def openDoor(request):
    doorObj = door.objects.filter(doorName="home")
    controller(doorObj,'rellim')
    return HttpResponse("door has been opened!")

def closeDoor(request):
    return
