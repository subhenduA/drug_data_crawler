import os
import json
import pandas as pd
import numpy as np

'''
recursively go through the directories and normalize each of the drug file ..
use panda df parallelizer to distribute the work 
on each drug file map to transform the data 
Utlimately store the data in simple flat files for easy access to flask  
'''
class ParallelNormalizer:
	column_list = ['type','target','source','pronunciation','trade_names','ahfs_drugs_com','license_data','pregnancy__category','routes_of__administration','atc_code','legal_status','bioavailability','biological_half_life','cas_number','drugbank','chemspider','unii','kegg','chembl','formula','molar_mass']
	global_df = pd.DataFrame(dtype=np.str, columns=column_list)
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
		# insert to global_df


if __name__ == '__main__':
	Normalizer().search_process_drug_json_files("/Users/saich/Documents/Personal/MyRepo/drug_data_crawler/output")