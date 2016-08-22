from .CloudResource import *

class Theme(CloudResource):
	"""
	Represents a Theme resource.
	https://cloud-developer.weebly.com/theme.html
	"""

	def __init__(self, theme_id, user_id, data=None):
		self.theme_id = int(theme_id)
		CloudResource.__init__(self, data)

	def _get(self):
		#theme doesn't have a GET method
		pass

	def id(self):
		"""Returns the theme_id"""
		return self.theme_id
