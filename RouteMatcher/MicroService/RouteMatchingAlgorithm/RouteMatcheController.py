####### Importing Basic Packages ############
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json 

########### Importing the Matching Algorithm #########
from RouteAlgo import isRouteCompatible

#################### Initialising FireBase ##################
cred = credentials.Certificate('service-account.json')
# Initialize the app with a service account, granting admin privileges
app=firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://kute-ec351.firebaseio.com/'
})

# As an admin, the app has access to read and write all data, regradless of Security Rules
#################### Create references to Firebase database ##############
friend_ref = db.reference('Friends')
route_ref=db.reference("Routes")
user_ref=db.reference("Users")

######## End Of Firebase Initialisation

user_name="Vishrut Kohli"
user_friends=[]


try:
	user_friends_dict=json.dumps(friend_ref.order_by_key().equal_to(user_name).get())
	user_friends_dict=json.loads(user_friends_dict)
	user_friends=user_friends_dict[user_name].keys()
	print user_friends[0]

	################ query for friend Routes #################
	friend_routes={}
	friend_routes=route_ref.order_by_key().equal_to(user_friends[1]).get()
	friend_route_list=friend_routes.values()
	print friend_route_list[0].values()[0]["source_cords"]

	
except Exception as e:
	print "Exception while retrieving from firebase :",e



