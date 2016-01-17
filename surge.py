import requests
import math
import time
import os.path
import config as cfg

#Set API keys from configuration file
server_token = cfg.server_token

#Define the uber types that we'll search for
uber_types = ['uberX', 'uberXL', 'uberSELECT', 'UberBLACK', 'UberSUV']

#Set up a few locations for different trips:
locations = {}
locations['DNA_lounge'] = {
	'latitude': 37.7589,
	'longitude': -122.4125
}
locations['Marina'] = {
	'latitude': 37.8007,
    'longitude': -122.4447
}
locations['Financial_district'] = {
	'latitude': 37.7960,
	'longitude': -122.4121
}
locations['Union_square'] = {
	'latitude': 37.7874,
	'longitude': -122.4104
}
locations['Mission'] = {
	'latitude': 37.7576,
    'longitude': -122.4105
}
locations['The_Castro'] = {
	'latitude': 37.7625,
	'longitude': -122.4373
}
locations['Noe_valley'] = {
	'latitude': 37.7500,
	'longitude': -122.4316
}
locations['Outer_sunset'] = {
	'latitude': 37.7621,
	'longitude': -122.5114
}
locations['Dogpatch'] = {
	'latitude': 37.7604,
	'longitude': -122.3918
}
locations['Palo_Alto'] = {
	'latitude': 37.4061,
    'longitude': -122.1142
}
locations['SFO'] = {
	'latitude': 37.6213,
	'longitude': -122.3811
}
locations['SJC'] = {
	'latitude': 37.3664,
	'longitude': -121.9257
}
#Template for adding new locations:
#locations[''] = {
#	'latitude': 
#	'longitude':
#}

#In order to get a surge multiplier, we need to enter a start/end location for the trip, however
#the surge price only depends on your starting location (as far as I can tell). I'll keep in
#the functionality of looking at arbitrary trips in case this changes and for verification
#purposes, which can be enables by setting connect_different_locations to True.
connect_different_locations = False

trips = {}
if(connect_different_locations):
	#Define the set of path's to collect surge data on
	path_connector = '->' #String that will connect locations in our dictionary, eg. "Mission->Marina"
	#Explicit definition of paths:
	#trips_list = ['DNA'+path_connector+'Marina', 'Marina'+path_connector+'DNA', 'Mission'+path_connector+'Marina', 'Marina'+path_connector+'Mission', 'Mission'+path_connector+'Palo_Alto', 'Marina'+path_connector+'Palo_Alto', 'DNA'+path_connector+'Palo_Alto', 'Palo_Alto'+path_connector+'Mission', 'Palo_Alto'+path_connector+'Marina', 'Palo_Alto'+path_connector+'DNA']

	#Connect all of the endpoints specified in the locations list:
	trips_list = []
	for start_location in locations:
		for end_location in locations:
			trips_list.append(start_location+path_connector+end_location)

	#Set up the dictionary that will hold all the trip and surge multiplier data:
	for trip in trips_list:
		trips[trip] = {
			'start_latitude': locations[trip[0:trip.find(path_connector)]]['latitude'],
			'start_longitude': locations[trip[0:trip.find(path_connector)]]['longitude'],
			'end_latitude': locations[trip[trip.find(path_connector)+len(path_connector):len(trip)]]['latitude'],
			'end_longitude': locations[trip[trip.find(path_connector)+len(path_connector):len(trip)]]['longitude'],
			'surge_data': {}
		}
#Otherwise just examine trips from the same starting/ending points:
else:
	for loc in locations:
		trips[loc] = {
			'start_latitude': locations[loc]['latitude'],
			'start_longitude': locations[loc]['longitude'],
			'end_latitude': locations[loc]['latitude'],
			'end_longitude': locations[loc]['longitude'],
			'surge_data': {}
		}

print trips

#Specify the url to query for the API request
#url = 'https://api.uber.com/v1/products'
url = 'https://api.uber.com/v1/estimates/price'

#Set up the output file to store the data
output_file_name = "Surge_data_Jan16_2016.txt"
#If the output file already exists, don't write a header and just start appending data to it. If the file
#does not exist, then create it and put a header on top of it.
if(not os.path.isfile(output_file_name)):
	output_file = open(output_file_name, "w")
	output_file.write('{0:50}'.format('Each route has Uber ride types in the order:'))
	for uber_type in uber_types:
		output_file.write('{0:15}'.format(uber_type))
	output_file.write('\n')
	output_file.write('{0:30}'.format('Time'))
	for trip in trips.keys():
		output_file.write('{0:30}'.format(trip))
	#output_file.write('{0:30} {1:30} {2:30} {3:30} {4:30} {5:30} {6:30} {7:30} {8:30} '.format("Time", "DNA_to_Marina", "Marina_to_DNA", "Mission_to_Palo_Alto", "Palo_Alto_to_Mission", "Mission_to_Mission", "Marina_to_Marina", "Palo_Alto_to_Palo_Alto", "DNA_to_DNA"))
	output_file.write('\n')
else:
	output_file = open(output_file_name, "a")

#Collect data forever!
while(True):
	#Initialize the surge data for each car type in each trip
	for trip in trips.keys():
		for uber_type in uber_types:
			trips[trip]['surge_data'][uber_type] = 0.0

	#Go through each of the trips and find the surge multipliers for each car type:
	for trip in trips.keys():
		params = {'server_token':server_token, 'start_latitude':trips[trip]['start_latitude'], 'start_longitude':trips[trip]['start_longitude'], 'end_latitude':trips[trip]['end_latitude'], 'end_longitude':trips[trip]['end_longitude']}
		response = requests.get(url, params)
		data = response.json()
		for uber_type in uber_types:
			car_key = [index for index, val in enumerate(data['prices']) if val['localized_display_name'] == uber_type]
			if len(car_key) > 0:
				trips[trip]['surge_data'][uber_type] = data['prices'][car_key[0]]['surge_multiplier']

	print 'trips:'
	print trips

	#output_file.write('{0:30} {1:29.1f} {2:29.1f} {3:29.1f} {4:29.1f} {5:29.1f} {6:29.1f} {7:29.1f} {8:29.1f}'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()), multiplier_dna_to_marina, multiplier_marina_to_dna, multiplier_mission_to_palo_alto, multiplier_palo_alto_to_mission, multiplier_mission_to_mission, multiplier_marina_to_marina, multiplier_palo_alto_to_palo_alto, multiplier_dna_to_dna))
	output_file.write('{0:30}'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
	for trip in trips.keys():
		for uber_type in uber_types:
			output_file.write('{0:5.1f}'.format(trips[trip]['surge_data'][uber_type]))
		output_file.write('     ')
	output_file.write('\n')
	time.sleep(60)