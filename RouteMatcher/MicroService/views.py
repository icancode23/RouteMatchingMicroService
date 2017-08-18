from django.shortcuts import render
from MicroService.tasks import rebuild_search_index
from django.http import HttpResponse 
# Create your views here.
## test function 
def check(request):
	return HttpResponse("Yes this works")