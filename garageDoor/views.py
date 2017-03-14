from django.shortcuts import render
from django.http import HttpResponse
from garageDoor.models import door, openEvent, closeEvent
from garageDoor.services import controller
# Create your views here.
def index(request):
    return HttpResponse("Welcome To Prime Ingenuitys Garage door division")

def openDoor(request):
    c = controller()
    result = c.open()
    if result == True:
        return HttpResponse("door has been opened!")
    else:
        return HttpResponse("the Door failed to open or something")

def closeDoor(request):
    c = controller()
    result = c.close()
    if result == True:
        return HttpResponse("door has been Closed")
    else:
        return HttpResponse("the Door failed to close or something")

def forceCloseDoor(request):
    c = controller()
    result = c.forceClose()
    if result == True:
        return HttpResponse("door has been Closed")
    else:
        return HttpResponse("the Door failed to close or something")

def statusCheck(request):
    c = controller()
    result = c.statusCheck()
    if result == 1:
        return HttpResponse("The Door is Open")
    elif result == 0:
        return HttpResponse("The Door is closed")