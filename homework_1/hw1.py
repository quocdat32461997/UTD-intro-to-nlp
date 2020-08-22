"""
hw1.py - module to implement Python codes to extract text and parse to Person object
"""

import re

class Person:
	"""
	Person - class to get input data and parse them to standardized Person object
	"""
	def __init__(self, data):
		"""
		Inputs:
			data - str
		"""
		parsed_data = self.preprocess(data)
		self.last_name = parsed_data[0]
		self.first_name = parsed_data[1]
		self.middle_initial = parsed_data[2]
		self.id = parsed_data[3]
		self.phone = parsed_data[4]
		super(Person, self).__init__()

	def get(self):
		"""
		get - function to return Person object's properties and print Person object
		"""
		print(self.last_name, self.first_name, self.middle_initial, self.id, self.phone)
		return self.last_name, self.first_name, self.middle_initial, self.id, self.phone

	def preprocess(self, input):
		# strip white space
		input = input.strip()
		
		# tokenize by delimiter = ','
		tokens = input.split(',')

		# tokens in order: last_name, first_name, middle initial, id, and phone_no

		# processing: last_name, and first name, and middle initial
		for token in tokens[:3]:
			if token:
				token = token.lower()
				token[0] = token[0].upper()
			else:
				token = 'X' # if name missing, return X instead

		# processing: id
		id_pattern = '/[^A-Za-z][A-Za-z][0-9]{4}/'
		while not re.match(id_pattern, tokens[3]):
			print('ID invalid', tokens[3])
			tokens[3] = input('ID is two letters followed by 4 digits\nPlease enter a valid id:')

		# processing phone_no
		phone_pattern = '/^[0-9]{3}-[0-9]{3}-[0-9]{4}/'
		if not re.match(phone_pattern, tokens[4]):
			# remove all non-numeric characters
			tokens[4] = re.sub('[^0-9]', '', tokens[4])

			# convert to preferred format
			tokens[4] = str(tokens[4][:3]) + '-' + str(tokens[3:6]) + '-' + str(tokens[6:])
		return tokens

def main():
	# read data
	with open('data.csv', 'r') as f:
		data = f.readlines()[1:] # ignore header
	
	# loop over to parse multiple Person objects
	person = []
	for person in data:
		persons.append(Person(person))

if __name__ == '__main__':
	main()
