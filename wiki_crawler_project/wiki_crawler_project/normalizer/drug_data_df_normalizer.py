import os
import json
import pandas as pd
import numpy as np
from multiprocessing import Pool
from transformers import TransformFunctions

'''
A) This class recursively go through the source directories and normalize each of the drug file. Remember
drug files are stored in as .json files in hierarchical directories
B) The code loads the json contents in dataframe .
C) Wrangles inidivdiual fields in data frame using 'multiprocessing'
D0 Store the wrangled data in a single json file for easy access to flask  
'''
class ParallelNormalizer:
	column_list = ['type','target','source','pronunciation','trade_names','ahfs_drugs_com','license_data','pregnancy__category','routes_of__administration','atc_code','legal_status','bioavailability','biological_half_life','cas_number','drugbank','chemspider','unii','kegg','chembl','formula','molar_mass']
	global_df = pd.DataFrame(dtype=np.str, columns=column_list)

	def __init__(self, dircectory=None):
		self.dir_path = dircectory

	'''
	Recursively searches the source directory for drug json files
	'''
	def search_process_drug_json_files(self, dirctory):
		files = os.listdir(dirctory)
		for fl in files:
			path = os.path.join(dirctory,fl)
			if os.path.isdir(path):
				self.search_process_drug_json_files(path)
			elif path.endswith(".json"):
				self.load_raw_json(path)
		return

	def load_raw_json(self, json_filepath):
		json_file = open(json_filepath)
		wiki_name = json_filepath.split("/")[-1].replace(".json", "")
		json_data = json.load(json_file)
		# this is the normalized dict structure 
		normalized_dict = {'wiki_drug_name': wiki_name, 'type' : '', 'target' : '','source' : '','pronunciation' : '','trade_names' : '','ahfs_drugs_com' : '','license_data' : '','pregnancy__category' : '','routes_of__administration' : '','atc_code' : '','legal_status' : '','bioavailability' : '','biological_half_life' : '','cas_number' : '','drugbank' : '','chemspider' : '','unii' : '','kegg' : '','chembl' : '','formula' : '','molar_mass' : ''}
		# standardizes the key name to map it to normalized dict structure 
		for key in json_data.keys():
			column_name = key.replace(" ", "_").replace('\n', '_').replace('/', '_').replace('.', '_').replace('-', '_').lower()
			if column_name in self.column_list:
				normalized_dict[column_name] = json_data[key]

		# appends data to single data frame , only data tables not much dats fits into memroy 
		self.global_df = self.global_df.append(normalized_dict, ignore_index=True)
	
	def normalize_and_save(self):
		# this piece of code to be executed without multiprocessing 
		'''
		self.global_df['biological_half_life_min'] = self.global_df['biological_half_life'].map(lambda x : self.biological_half_life_min(x))
		self.global_df['biological_half_life_max'] = self.global_df['biological_half_life'].map(lambda x : self.biological_half_life_max(x))
		'''
		# this piece of code executes when multiprocessing used
		num_partitions = 4 #number of partitions to split dataframe
		num_cores = 2 #number of cores on your machine
		df_split = np.array_split(self.global_df, num_partitions)
		pool = Pool(num_cores)
		self.global_df = pd.concat(pool.map(self.normalize_biological_half_life, df_split))
		pool.close()
		pool.join()
		
		# TODO : calculate few stats now and save it somewhere

		# saves the dataframe as json so that flask server can use it for query 
		self.global_df.set_index(['wiki_drug_name'], inplace=True)
		json_data = json.loads(self.global_df.to_json(orient='index'))
		normalized_drug_file_path = '%s/drug_data_normalized.json' % self.dir_path
		with open(normalized_drug_file_path, 'w') as f:
			json.dump(json_data, f)

	'''
	The apply function for parallel processing
	'''
	def normalize_biological_half_life(self, df):
		df['biological_half_life_min'] = df['biological_half_life'].map(lambda x : TransformFunctions.biological_half_life_min(x))
		df['biological_half_life_max'] = df['biological_half_life'].map(lambda x : TransformFunctions.biological_half_life_max(x))
		#TODO : add biological avg. 
		return df

if __name__ == '__main__':
	# TODO remove the hard coding on filepath 
	nm = ParallelNormalizer("/Users/saich/Documents/Personal/MyRepo/drug_data_crawler/output")
	nm.search_process_drug_json_files(nm.dir_path)
	nm.normalize_and_save()