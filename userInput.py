#!/usr/bin/env python
# coding: utf-8

class userInput:
	def __init__(self):
		self.company_lst = None
		self.location_lst = None
		self.title_lst = None
		self.username = None
		self.password = None

	def get_username(self):
		return self.username

	def get_password(self):
		return self.password

	def get_companies(self):
		return self.company_lst

	def get_locations(self):
		return self.location_lst

	def get_titles(self):
		return self.title_lst

	def set_username(self, username):
		self.username = username

	def set_password(self, password):
		self.password = password

	def set_companies(self, company_string):
		if ',' not in company_string:
			self.company_lst = [company_string]
		else:
			self.company_lst = input_to_list(company_string)

	def set_locations(self, location_string):
		if ',' not in location_string:
			self.location_lst = [location_string]
		else:
			self.location_lst = input_to_list(location_string)

	def set_titles(self, title_string):
		if ',' not in title_string:
			self.title_lst = [title_string]
		else:
			self.title_lst = input_to_list(title_string)


	def input_to_list(input_string):
		return [_input.strip() for _input in input_string.split(",")]

	def __str__(self):
		return_str = "\nLinkedin Search Parameters:\n\nUsername:{}\nCompanies:{}\nTitles:{}\nLocations:{}\n".format(
			self.get_username(), self.get_companies(), self.get_titles(), self.get_locations())

		return return_str






