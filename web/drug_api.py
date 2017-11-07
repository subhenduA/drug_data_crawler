from flask import Flask
import csv
import json
app = Flask(__name__)

@app.route('/drug_info/<drug_name>')
def json_drug_data(drug_name):
	# TODO keep the index dict instantiated once and use it for all the requests, it's read only entity
	index_dict = {} 
	with open('/Users/saich/Documents/Personal/MyRepo/drug_data_crawler/output/drug_index.csv', newline='') as indexfile:
		reader = csv.reader(indexfile, delimiter='|')
		for row in reader:
			index_dict[row[0].lower()]= row[1]
	try:
		json_file = open(index_dict[drug_name.lower()])
		json_data = json.load(json_file)
		return json.dumps(json_data)
	except KeyError as err:
		return 'drug name %s not found in database' % drug_name


if __name__ == "__main__":
 	app.run(host='0.0.0.0', port=80, debug=True)
 	# take the index file as optinos through options parser 