from .CloudResource import *

class FormEntry(CloudResource):
	"""
	Represents a FormEntry resource.
	https://cloud-developer.weebly.com/form-entry.html
	"""

	def __init__(self, form_entry_id, user_id, site_id, form_id, data=None):
		self.user_id = int(user_id)
		self.site_id = int(site_id)
		self.form_id = int(form_id)
		self.form_entry_id = int(form_entry_id)
		self._endpoint = "user/{0}/site/{1}/form/{2}/entry/{3}".format(
			self.user_id,
			self.site_id,
			self.form_id,
			self.form_entry_id
		)
		CloudResource.__init__(self, data)

	def id(self):
		"""Return the form_entry_id"""
		return self.form_entry_id
