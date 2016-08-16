import json
import math
import re

# Try getting Python requests module http://docs.python-requests.org/en/master/
try:
	import requests
except ImportError:
	raise ImportError("Requests module not available. Use 'pip install requests'.")

from .Exceptions import *

class WeeblyCloudResponse(object):
	"""
	All requests made in CloudClient return an object of this type. If the
	response is paginated, then WeeblyCloudResponse will allow paging through
	results.
	"""

	def __init__(self, session, response):
		self.page_size = None
		self.max_page = None
		self.current_page = None
		self.records = None
		self.is_paginated = False

		self.__session = session
		self.__response = response
		self.__refresh()
		self.__first_iter = True

	def __iter__(self):
		"""Returns the response as an interable."""
		if not self.is_paginated:
			raise PaginationError("The response is not paginated.")
		return self

	def __next__(self):
		"""Allows paging through the response as an iterable in Python 3"""
		return next()

	def __len__(self):
		"""Returns the number of pages in the result or None if not paginated"""
		if not self.is_paginated:
			return None
		else:
			return self.max_page

	def __str__(self):
		"""Return the JSON of the current page"""
		return json.dumps(self.json)

	def next(self):
		"""Allows paging through the response as an iterable"""
		if self.__first_iter:
			self.__first_iter = False
			return self.json
		else:
			has_next_page = self.next_page()
			if has_next_page:
				return self.json
			raise StopIteration

	def dict(self):
		"""Gets the response as a dict"""
		return self.json

	def next_page(self):
		"""Get the next page, return True on success, False on failure."""

		if not self.is_paginated:
			raise PaginationError("The response is not paginated.")
		if self.current_page >= self.max_page:
			return False

		next_request = self.__prepare_request(self.current_page + 1)
		self.__response = self.__session.send(next_request)

		self.__refresh()
		return True

	def previous_page(self):
		"""Get the previous page, return True on success, False on failure."""

		if not self.is_paginated:
			raise PaginationError("The response is not paginated.")
		if self.current_page <= 1:
			return False

		next_request = self.__prepare_request(self.current_page - 1)
		self.__response = self.__session.send(next_request)
		self.__refresh()
		return True

	def __refresh(self):
		"""Refresh the object based on the new Response."""

		self.status_code = self.__response.status_code

		# Handle errors. Sometimes there may not be a response body (which is why ValueError)
		# must be caught.
		try:
			if (self.__response.status_code not in [200,204]) or 'error' in self.__response.json():
				error = self.__response.json()
				raise ResponseError(error['error']['message'], error['error']['code'])
		except ValueError:
			# Sometimes DELETE returns nothing. When this is the case, it will have a status code 204
			if self.__response.request.method is not "DELETE" and self.__response.status_code is not 204:
				raise ResponseError("Unknown error occured.", self.__response.status_code)

		# Get information on paging if response is paginated
		if 'X-Resultset-Total' in self.__response.headers and self.__response.headers['X-Resultset-Total'] > self.__response.headers['X-Resultset-Limit']:
			self.is_paginated = True
			self.records = int(self.__response.headers.get('X-Resultset-Total'))
			self.page_size = int(self.__response.headers['X-Resultset-Limit'])
			self.current_page = int(self.__response.headers['X-Resultset-Page'])
			self.max_page = int(math.ceil(float(self.records)/int(self.page_size)))

		# Save the content of the request
		try:
			self.json = self.__response.json()
		except ValueError:
			# Sometimes DELETE returns nothing. When this is the case, it will have a status code 204
			if self.__response.request.method == "DELETE" and self.__response.status_code is 204:
				self.json = {"success":True}
			else:
				raise ValueError("No JSON object could be decoded" + self.__response.request.method)

	def __prepare_request(self, page):
		"""Updates the existing request based on the new page. Returns the new PreparedRequest."""
		# Replace the page parameter if it exists and add it if it doesn't exist
		page_regex = re.compile("(?<=[\\&\\?]page=)\\d*")
		regex_res = page_regex.subn(str(page),self.__response.request.url)

		if regex_res[1] == 0:
			self.__response.request.prepare_url(self.__response.request.url, {'page': str(page)})
		else:
			self.__response.request.url = regex_res[0]

		return self.__response.request
