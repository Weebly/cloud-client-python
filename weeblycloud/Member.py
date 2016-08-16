from .SaveableResource import *
from .Deleteable import *

class Member(SaveableResource, Deleteable):
	"""
	Represents a Member resource.
	https://cloud-developer.weebly.com/member.html
	"""

	def __init__(self, member_id, user_id, site_id, data=None):
		self.user_id = int(user_id)
		self.site_id = int(site_id)
		self.member_id = int(member_id)
		self._endpoint = "user/{0}/site/{1}/member/{2}".format(self.user_id, self.site_id, self.member_id)
		SaveableResource.__init__(self, data)

	def id(self):
		"""Return the member_id"""
		return self.member_id
