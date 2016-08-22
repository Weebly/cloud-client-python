from .cloudclient import WeeblyCloudResponse

class PaginatedList(object):
	"""An interable list of CloudResource objects"""

	def __init__(self, response, the_type, other_ids, this_id_name):
		self.__response = response
		self.__refresh()

		self.type = the_type
		self.__this_id_name = this_id_name
		self.__other_ids = other_ids
		self.__cursor = 0

	def __iter__(self):
		"""Return the iterator."""
		return self

	def __len__(self):
		"""Returns the number of records"""
		try:
			return self.__response.records
		except AttributeError:
			return len(self.list)

	def __next__(self):
		"""This allows compatibility with Python 3"""
		return self.next()

	def next(self):
		"""
		Get the next element in a list of elements. Requests the next page
		of results as needed.
		"""

		# If the end of the page is reached, either get the next page or stop
		# iteration
		if self.__cursor >= len(self.list):

			# If the result isn't paginated, no need to try to get next page
			if not self.__response.is_paginated:
				raise StopIteration

			# Get the next page, stop iteration if it doesn't exist
			has_next_page = self.__response.next_page()
			if not has_next_page:
				raise StopIteration

			self.__refresh

			# reset the cursor to the beginning of the page
			self.__cursor = 0
		# get an item and it's ID
		item = self.list[self.__cursor]
		this_id = item[self.__this_id_name]

		self.__cursor += 1

		# create an item of self.type's type, unpacking the tuple other_ids using
		# Python's magical powers...
		return self.type(this_id, *self.__other_ids, data=item)

	def __refresh(self):
		"""Refresh the object based on the new a new response."""

		# Sometimes the API responds with a list while other times it responds
		# with a dictionary containing a list.
		if isinstance(self.__response.json, dict):
			self.list = list(self.__response.json.values())[0]
		else:
			self.list = self.__response.json
