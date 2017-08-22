from django.shortcuts import render
from MicroService.tasks import checkPath
from django.http import HttpResponse 

# Create your views here.
## test function 
def check(request):
	checkPath.delay()
	return HttpResponse("Yes this works")

## Function To send notifications to clients 
def sendNotifications(request):
	## retrieve the get parameters
	owner=request.GET.get("Owner")
	rider=request.GET.get("Rider")
	notifType=request.GET.get("notifType")
	return HttpResponse(owner +rider + notifType)


