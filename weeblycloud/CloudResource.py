from .cloudclient import CloudClient
import json

class CloudResource(object):
	"""
	A base resource that all other resources inherit from.
	"""

	def __init__(self, data=None):
		self.client = CloudClient()
		self.properties = {}

		# If data is passed in, don't make a request.
		if data:
			self.properties = data
			self._got = False
		else:
			self._get()
			self._got = True

	def get_property(self,prop):
		"""Get a property of the object. Return None if property does not exist."""
		try:
			return self.properties[prop]
		except KeyError:
			# Sometimes if data is passed in, the object may not include a
			# property that should be there if a get request was made to the
			# server. This makes that get request and then tries again.
			if self._got:
				return None
			else:
				self._got = True
				self._get()
				return self.get_property(prop)

	def __str__(self):
		"""Return a JSON representation of object's properties."""
		return json.dumps(self.properties)

	def _get(self):
		"""
		This method will make a call to get the parameters for the resource.
		"""
		response = self.client.get(self._endpoint)
		self.properties = response.json

	def id(self):
		"""
		This method will return the ID of the object.
		"""
		raise NotImplementedError("Method not available for this endpoint.")
