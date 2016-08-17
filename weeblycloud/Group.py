from .SaveableResource import *
from .Deleteable import *

class Group(SaveableResource, Deleteable):
	"""
	Represents a Group resource.
	https://cloud-developer.weebly.com/group.html
	"""

	def __init__(self, group_id, user_id, site_id, data=None):
		self.user_id = int(user_id)
		self.site_id = int(site_id)
		self.group_id = int(group_id)
		self._endpoint = "user/{0}/site/{1}/group/{2}".format(
			self.user_id,
			self.site_id,
			self.group_id
		)
		SaveableResource.__init__(self, data)

	def id(self):
		"""Return the group_id"""
		return self.group_id
