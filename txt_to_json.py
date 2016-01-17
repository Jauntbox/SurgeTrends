'''Helper script to convert pre-collected text data into JSON format to make plotting with d3.js easier'''

import json

file_name = 'Surge_data_Jan15_2016'

#First read the text file
infile = open(file_name+'.txt','r')
uber_types = infile.readline().split()
uber_types = uber_types[len(uber_types)-5:len(uber_types)]
headers = infile.readline()
headers_list = headers.split()
data = infile.readlines()
infile.close()

#Next, put it into a dictionary (just as in the iPython notebook)
data_dict = {}
data_dict[headers_list[0]] = []
for item in headers_list[1:len(headers_list)]:
    data_dict[item] = {}
    for uber_type in uber_types:
        data_dict[item][uber_type] = []
for line in data:
    dataline = line.split()
    dataline[0:2] = [dataline[0] + ' ' + dataline[1]]
    data_dict[headers_list[0]].append(dataline[0])
    for trip_index,trip in enumerate(headers_list[1:len(headers_list)]):
        for uber_type_index,uber_type in enumerate(uber_types):
            data_dict[trip][uber_type].append(dataline[trip_index*len(uber_types) + uber_type_index + 1])

data_array = []
for line in data:
    dataline = line.split()
    dataline[0:2] = [dataline[0] + ' ' + dataline[1]]
    dict_to_insert = {}
    dict_to_insert[headers_list[0]] = dataline[0]
    for header_index,header_item in enumerate(headers_list[1:len(headers_list)]):
        dict_to_insert[header_item] = {}
        for uber_type_index,uber_type in enumerate(uber_types):
            dict_to_insert[header_item][uber_type] = dataline[header_index*len(uber_types) + uber_type_index + 1]
    data_array.append(dict_to_insert)

#Finally output it in JSON format
output_file = open(file_name+'.json', "w")
#output_file.write(json.dumps(data_dict))
output_file.write(json.dumps(data_array))
output_file.close()