from .CloudResource import *

class Deleteable(object):
	"""
	CloudResource objects may inherit from this to gain the
	ability to be deleted.
	"""

	def __init__(self):
		pass

	def delete(self):
		"""Deletes the resource"""
		response = self.client.delete(self._endpoint)
		return bool(response.json['success'])
