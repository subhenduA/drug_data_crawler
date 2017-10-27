import json
import MySQLdb
import os

# This class is responsible for processing drug data stored in json file, 
# filters the relevant elements from json file, 
# normalize the key name to a database column name,
# standardizes the values so that it can be loaded
# Uploads the data into a mysql table
class Normalizer:
	column_list = ['type','target','source','pronunciation','trade_names','ahfs_drugs_com','license_data','pregnancy__category','routes_of__administration','atc_code','legal_status','bioavailability','biological_half_life','cas_number','drugbank','chemspider','unii','kegg','chembl','formula','molar_mass']
	
	def search_process_drug_json_files(self, directory):
		files = os.listdir(directory)
		for fl in files:
			path = os.path.join(directory,fl)
			if os.path.isdir(path):
				self.search_process_drug_json_files(path)
			elif path.endswith(".json"):
				self.normalize_and_load(path)
		return

	def normalize_and_load(self, json_filepath):
		json_file = open(json_filepath)
		wiki_name = json_filepath.split("/")[-1].replace(".json", "")
		json_data = json.load(json_file)
		column_name_list , column_value_list = ['wiki_name'], [self.normalize_value(wiki_name)]
		for key in json_data.keys():
			column_name = key.replace(" ", "_").replace('\n', '_').replace('/', '_').replace('.', '_').replace('-', '_').lower()
			if column_name in self.column_list:
				column_name_list.append(column_name)
				column_value_list.append(self.normalize_value(json_data[key]))
		insert_query = "INSERT INTO drug_details (%s) VALUES (%s);" %(','.join(column_name_list), ','.join(column_value_list))
		print("%s" %insert_query)
		conn = MySQLdb.connect(host= "localhost", db="test")
		conn.cursor().execute(insert_query)
		conn.commit()

	def normalize_and_save(self):
		pass

	def normalize_value(self, raw_value):
		if raw_value == None or raw_value == '':
			return '\'\''
		return ''.join(["'", raw_value.replace("'", "\\'").replace("(", "\(").replace(")", "\)").replace(",", "\,").replace("/","\/"), "'"])

if __name__ == '__main__':
	Normalizer().search_process_drug_json_files("/Users/saich/Documents/Personal/MyRepo/drug_data_crawler/output")