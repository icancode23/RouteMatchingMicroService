from django.shortcuts import render
from MicroService.tasks import checkPath,postNotifications
from django.http import HttpResponse 

# Create your views here.

## Test Endpoint
def check(request):
	checkPath.delay()
	return HttpResponse("Yes this works")

######################## Endpoint for route matching #####################################
def matchRoute(request):
	### Retrieve the get parameters ################
	owner=request.GET.get("Owner")
	rider=request.GET.get("Rider")
	### The variable below indicates whether the  request for matching the route came from a ride host or rider ############
	initiator=request.GET.get("Initiator")

	################ invoke Celery task to start matching Trips and routes #########
	#checkPath.delay(owner,rider,initiator)
	return HttpResponse(owner+rider+initiator)


## Endpoint To send notifications to clients 
def sendNotifications(request):
	## retrieve the get parameters
	owner=request.GET.get("Owner")
	rider=request.GET.get("Rider")
	notifType=request.GET.get("notifType")
	
	############# invoke celery task to send out notifications ##########
	postNotifications.delay(owner,rider,notifType)

	return HttpResponse("{Status:OK}")

