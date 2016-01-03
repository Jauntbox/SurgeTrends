import requests
import math
import time
import config as cfg

#Set API keys from configuration file
server_token = cfg.server_token

#Define the uber types that we'll search for
uber_types = ['uberX', 'uberXL', 'uberSELECT', 'UberBLACK', 'UberSUV']

#Set up a few start/end locations for different trips:

#Number of locations to be tracked
#num_trips = 4
#trips = [None]*num_trips

trips = {}
trips['DNA_to_Marina'] = {
	'start_latitude': 37.7589,
    'start_longitude': -122.4125,
    'end_latitude': 37.8007,
    'end_longitude': -122.4447,
    'surge_data': {}
    }
trips['Marina_to_DNA'] = {
	'end_latitude': 37.7589,
    'end_longitude': -122.4125,
    'start_latitude': 37.8007,
    'start_longitude': -122.4447,
    'surge_data': {}
    }
trips['Mission_to_Palo_Alto'] = {
	'start_latitude': 37.7576,
    'start_longitude': -122.4105,
    'end_latitude': 37.4061,
    'end_longitude': -122.1142,
    'surge_data': {}
    }
trips['Palo_Alto_to_Mission'] = {
	'end_latitude': 37.7576,
    'end_longitude': -122.4105,
    'start_latitude': 37.4061,
    'start_longitude': -122.1142,
    'surge_data': {}
    }
trips['Mission_to_Mission'] = {
    'end_latitude': 37.7576,
    'end_longitude': -122.4105,
    'start_latitude': 37.7576,
    'start_longitude': -122.4105,
    'surge_data': {}
}
trips['Marina_to_Marina'] = {
    'end_latitude': 37.7589,
    'end_longitude': -122.4125,
    'start_latitude': 37.7589,
    'start_longitude': -122.4125,
    'surge_data': {}
}
trips['Palo_Alto_to_Palo_Alto'] = {
    'end_latitude': 37.4061,
    'end_longitude': -122.1142,
    'start_latitude': 37.4061,
    'start_longitude': -122.1142,
    'surge_data': {}
}
trips['DNA_to_DNA'] = {
    'start_latitude': 37.7589,
    'start_longitude': -122.4125,
    'end_latitude': 37.7589,
    'end_longitude': -122.4125,
    'surge_data': {}
}


parameters_dna_to_marina = {
    'server_token': server_token,
    'start_latitude': 37.7589,
    'start_longitude': -122.4125,
    'end_latitude': 37.8007,
    'end_longitude': -122.4447
}

parameters_marina_to_dna = {
    'server_token': server_token,
    'end_latitude': 37.7589,
    'end_longitude': -122.4125,
    'start_latitude': 37.8007,
    'start_longitude': -122.4447
}

parameters_mission_to_palo_alto = {
    'server_token': server_token,
    'start_latitude': 37.7576,
    'start_longitude': -122.4105,
    'end_latitude': 37.4061,
    'end_longitude': -122.1142
}

parameters_palo_alto_to_mission = {
    'server_token': server_token,
    'end_latitude': 37.7576,
    'end_longitude': -122.4105,
    'start_latitude': 37.4061,
    'start_longitude': -122.1142
}

parameters_mission_to_mission = {
    'server_token': server_token,
    'end_latitude': 37.7576,
    'end_longitude': -122.4105,
    'start_latitude': 37.7576,
    'start_longitude': -122.4105
}

parameters_marina_to_marina = {
    'server_token': server_token,
    'end_latitude': 37.7589,
    'end_longitude': -122.4125,
    'start_latitude': 37.7589,
    'start_longitude': -122.4125
}

parameters_palo_alto_to_palo_alto = {
    'server_token': server_token,
    'end_latitude': 37.4061,
    'end_longitude': -122.1142,
    'start_latitude': 37.4061,
    'start_longitude': -122.1142
}

parameters_dna_to_dna = {
    'server_token': server_token,
    'start_latitude': 37.7589,
    'start_longitude': -122.4125,
    'end_latitude': 37.7589,
    'end_longitude': -122.4125
}

#Specify the url to query for the API request
#url = 'https://api.uber.com/v1/products'
url = 'https://api.uber.com/v1/estimates/price'

#Set up the output file to store the data
output_file = open("Surge_data_Jan3_2016-2.txt", "w")
output_file.write('{0:50}'.format('Each route has Uber ride types in the order:'))
for uber_type in uber_types:
	output_file.write('{0:15}'.format(uber_type))
output_file.write('\n')
output_file.write('{0:30}'.format('Time'))
for trip in trips.keys():
	output_file.write('{0:30}'.format(trip))
#output_file.write('{0:30} {1:30} {2:30} {3:30} {4:30} {5:30} {6:30} {7:30} {8:30} '.format("Time", "DNA_to_Marina", "Marina_to_DNA", "Mission_to_Palo_Alto", "Palo_Alto_to_Mission", "Mission_to_Mission", "Marina_to_Marina", "Palo_Alto_to_Palo_Alto", "DNA_to_DNA"))
output_file.write('\n')

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

	#response = requests.get(url, params=parameters_dna_to_marina)
	#data = response.json()
	#multiplier_dna_to_marina = data['prices'][0]['surge_multiplier']
	#print 'DNA to Marina:', data['prices'][0]['surge_multiplier']

	#response = requests.get(url, params=parameters_marina_to_dna)
	#data = response.json()
	#multiplier_marina_to_dna = data['prices'][0]['surge_multiplier']

	#response = requests.get(url, params=parameters_mission_to_palo_alto)
	#data = response.json()
	#multiplier_mission_to_palo_alto = data['prices'][0]['surge_multiplier']
	#print 'Mission to Palo Alto:', data['prices'][0]['surge_multiplier']

	#response = requests.get(url, params=parameters_palo_alto_to_mission)
	#data = response.json()
	#multiplier_palo_alto_to_mission = data['prices'][0]['surge_multiplier']

	#response = requests.get(url, params=parameters_mission_to_mission)
	#data = response.json()
	#print data['prices'], len(data['prices'])
	#print data['prices'][0]['localized_display_name']
	#print data['prices'][1]['localized_display_name']
	#print data['prices'][2]['localized_display_name']
	#print data['prices'][3]['localized_display_name']
	#print data['prices'][4]['localized_display_name']
	#print data['prices'][5]['localized_display_name']
	#print data['prices'][6]['localized_display_name']
	#print data['prices'][7]['localized_display_name']
	#multiplier_mission_to_mission = data['prices'][0]['surge_multiplier']
	#print type(data['prices'])
	#for index, val in enumerate(data['prices']):
	#	print index, val['localized_display_name']
	#uberX_index = [index for index, val in enumerate(data['prices']) if val['localized_display_name'] == 'uberX'][0]
	#uberXL_index = [index for index, val in enumerate(data['prices']) if val['localized_display_name'] == 'uberXL'][0]
	#uberSELECT_index = [index for index, val in enumerate(data['prices']) if val['localized_display_name'] == 'uberSELECT'][0]
	#uberBLACK_index = [index for index, val in enumerate(data['prices']) if val['localized_display_name'] == 'UberBLACK'][0]
	#uberSUV_index = [index for index, val in enumerate(data['prices']) if val['localized_display_name'] == 'UberSUV'][0]
	#print 'Mission to Mission:', data['prices'][uberX_index]['surge_multiplier']
	#print 'Mission to Mission:', data['prices'][0]['surge_multiplier'], data['prices'][1]['surge_multiplier'], data['prices'][2]['surge_multiplier'], data['prices'][3]['surge_multiplier'], data['prices'][4]['surge_multiplier']

	#response = requests.get(url, params=parameters_marina_to_marina)
	#data = response.json()
	#multiplier_marina_to_marina = data['prices'][0]['surge_multiplier']

	#response = requests.get(url, params=parameters_palo_alto_to_palo_alto)
	#data = response.json()
	#multiplier_palo_alto_to_palo_alto = data['prices'][0]['surge_multiplier']

	#response = requests.get(url, params=parameters_dna_to_dna)
	#data = response.json()
	#multiplier_dna_to_dna = data['prices'][0]['surge_multiplier']

	#output_file.write('{0:30} {1:29.1f} {2:29.1f} {3:29.1f} {4:29.1f} {5:29.1f} {6:29.1f} {7:29.1f} {8:29.1f}'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()), multiplier_dna_to_marina, multiplier_marina_to_dna, multiplier_mission_to_palo_alto, multiplier_palo_alto_to_mission, multiplier_mission_to_mission, multiplier_marina_to_marina, multiplier_palo_alto_to_palo_alto, multiplier_dna_to_dna))
	output_file.write('{0:30}'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
	for trip in trips.keys():
		for uber_type in uber_types:
			output_file.write('{0:5.1f}'.format(trips[trip]['surge_data'][uber_type]))
		output_file.write('     ')
	output_file.write('\n')
	time.sleep(30)