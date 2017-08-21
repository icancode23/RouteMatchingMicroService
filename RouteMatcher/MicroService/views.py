from django.shortcuts import render
from MicroService.tasks import rebuild_search_index
from django.http import HttpResponse 
from tasks import rebuild_search_index
# Create your views here.
## test function 
def check(request):
	rebuild_search_index.delay()
	return HttpResponse("Yes this works")