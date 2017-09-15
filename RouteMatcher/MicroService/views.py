from django.shortcuts import render
from MicroService.tasks import checkPath,postNotifications
from django.http import HttpResponse 

# Create your views here.

## Test Endpoint
def check(request):
	checkPath.delay()
	return HttpResponse("Yes this works")

######################## Endpoint for route matching #####################################
def matchTrip(request):
	### Retrieve the get parameters ################
	person_id=request.GET.get("personId")
	### The variable below indicates whether the  request for matching the route came from a ride host or rider ############
	initiator=request.GET.get("Initiator")

	################ invoke Celery task to start matching Trips and routes #########
	checkPath.delay(person_id,initiator)
	return HttpResponse("{Status:OK}")


## Endpoint To send notifications to clients 
def sendNotifications(request):
	## retrieve the get parameters
	owner=request.GET.get("Owner")
	rider=request.GET.get("Rider")
	notifType=request.GET.get("notifType")
	
	############# invoke celery task to send out notifications ##########
	postNotifications.delay(owner,rider,notifType)

	return HttpResponse("{Status:OK}")

########### Function for tracker #######

import os
import sys
from pyvirtualdisplay import Display
from selenium import webdriver as wb
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup as bs
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
## The basic url for tracking on hcl's site 


###################### Function for creating a custom webdriver #############
def create_ch_driver():
  chrome_options = wb.ChromeOptions()
  chrome_options.add_argument("--no-sandbox")
  return wb.Chrome("/usr/local/bin/chromedriver", chrome_options=chrome_options)

def getTrackingStatus(tracking_no):
	####################### Create a Virtual Display for a VPS #######################
	display = Display(visible=0, size=(800, 600))
	display.start()
	driver=create_ch_driver()

	url="http://www.dhl.sc/en/express/tracking.html"

	##Formatted string for getting the exact tracking status as per the tracking number
	request_string="?AWB=%s&brand=DHL"%(tracking_no)
	ch=url+request_string
	print ch
	driver.get(ch)

	################## Wait for the page to load and give you the name of the constituency #####################################
	time.sleep(2)
	#WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[5]/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[2]/table[2]")))

	# elem = driver.find_element_by_xpath("/html/body/div[3]/div[5]/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[2]/table[2]")
	# source_code = elem.get_attribute("innerHTML")

	elem = driver.find_element_by_xpath("//*")
	source_code = elem.get_attribute("outerHTML")

	soup=bs(source_code,"html.parser")
	table=soup.find_all("table")[1]
	checkpoints=table.find_all("tr")
	checkpoints_dict={}
	date=""
	for cpoint in checkpoints:
		details=cpoint.find_all("td")
		if len(details)==0:
			details=cpoint.find_all("th")
			date=details[0].decode_contents(formatter="html")
		else:
			checkpoints_dict[details[0].decode_contents(formatter="html")]={"comment":details[1].decode_contents(formatter="html"),"place":details[2].decode_contents(formatter="html"),"date":date}

	driver.quit()

	jsonResponse=json.dumps(checkpoints_dict,indent=4)
	return jsonResponse
	# print jsonResponse
	


def trackShipment(request):
	tracking_no=request.GET.get("TrackingNo")
	resp=getTrackingStatus(tracking_no)
	return HttpResponse(resp,content_type="application/json")
	




