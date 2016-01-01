import requests
import math
import time
import config as cfg

#Set API keys from configuration file
server_token = cfg.server_token

#Set up a few start/end locations for different trips
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

#Specify the url to query for the API request
#url = 'https://api.uber.com/v1/products'
url = 'https://api.uber.com/v1/estimates/price'

#Set up the output file to store the data
output_file = open("Surge_data.txt", "w")
output_file.write('{0:30} {1:30} {2:30} {3:30} {4:30}'.format("Time", "DNA to Marina", "Marina to DNA", "Mission to Palo Alto", "Palo Alto to Mission"))
output_file.write('\n')

#Collect data forever!
while(True):
	response = requests.get(url, params=parameters_dna_to_marina)
	data = response.json()
	multiplier_dna_to_marina = data['prices'][0]['surge_multiplier']
	print 'DNA to Marina:', data['prices'][0]['surge_multiplier']

	response = requests.get(url, params=parameters_marina_to_dna)
	data = response.json()
	multiplier_marina_to_dna = data['prices'][0]['surge_multiplier']

	response = requests.get(url, params=parameters_mission_to_palo_alto)
	data = response.json()
	multiplier_mission_to_palo_alto = data['prices'][0]['surge_multiplier']
	print 'Mission to Palo Alto:', data['prices'][0]['surge_multiplier']

	response = requests.get(url, params=parameters_palo_alto_to_mission)
	data = response.json()
	multiplier_palo_alto_to_mission = data['prices'][0]['surge_multiplier']

	output_file.write('{0:30} {1:29.1f} {2:29.1f} {3:29.1f} {4:29.1f}'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()), multiplier_dna_to_marina, multiplier_marina_to_dna, multiplier_mission_to_palo_alto, multiplier_palo_alto_to_mission))
	output_file.write('\n')
	time.sleep(60)