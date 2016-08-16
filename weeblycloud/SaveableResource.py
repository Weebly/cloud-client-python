from .CloudResource import *

class SaveableResource(CloudResource):
	"""
	A saveable resource that all saveable resources inherit from.
	"""

	def __init__(self, data=None):
		self._changed = {}
		CloudResource.__init__(self, data)

	def set_property(self, prop, value):
		"""Set a property of the object. Will save on save() call. Return True on success, False otherwise."""
		try:
			self.properties[prop] = value
			self._changed[prop] = value
			return True
		except KeyError:
			# Sometimes if data is passed in, the object may not include a property that should be there
			# if a get request was made to the server. This makes that get request and then tries again.
			if not self._got:
				self._got = True
				self._get()
				return self.set_property(prop, value)
			else:
				return False

	def save(self):
		"""Saves changes to the resource"""
		self.client.patch(self._endpoint, content=self._changed)
		self._changed = {}
