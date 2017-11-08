from flask import Flask
import csv
import json
app = Flask(__name__)

@app.route('/drug_info/<drug_name>')
def json_drug_data(drug_name):
	# TODO keep the index dict instantiated once and use it for all the requests, it's read only entity
	json_file = open('/Users/saich/Documents/Personal/MyRepo/drug_data_crawler/web/drug_data_normalized.json') 
	drug_data = json.load(json_file)

	try:
		return json.dumps(drug_data[drug_name.lower()])
	except KeyError as err:
		return 'drug name %s not found in database' % drug_name


if __name__ == "__main__":
 	app.run(host='0.0.0.0', port=80, debug=True)
 	# take the index file as optinos through options parser 