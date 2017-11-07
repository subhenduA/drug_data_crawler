'''
 This class is intended to work on inndividual data elements on drug data 
 and creates normalized version of data
'''
class TransformFunctions:
	
	@classmethod
	def biological_half_life_min(cls, x):
		# TODO this function can be made more robust , doesn't take care of '2 to 10 hours' thing
		tokens = x.split(' ')
		for token in tokens:
			if '-' in token:
				return token[:token.find('-')]
			if '\u2013' in token:
				return token[:token.find('\u2013')]
		return None

	@classmethod
	def biological_half_life_max(cls, x):
		# TODO this function can be made more robust , doesn't take care of '2 to 10 hours' thing
		tokens = x.split(' ')
		for token in tokens:
			if '-' in token:
				return token[token.find('-')+1:]
			if '\u2013' in token:
				return token[token.find('\u2013')+1:]
		return None

	@classmethod
	def biological_half_life_avg(x):
		pass
		# TODO