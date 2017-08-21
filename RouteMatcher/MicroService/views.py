from django.shortcuts import render
from MicroService.tasks import rebuild_search_index
from django.http import HttpResponse 
from tasks import checkPath
# Create your views here.
## test function 
def check(request):
	checkPath.delay()
	return HttpResponse("Yes this works")