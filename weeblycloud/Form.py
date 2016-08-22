from .CloudResource import *
from .PaginatedList import *
from .FormEntry import *

class Form(CloudResource):
	"""
	Represents a Form resource.
	https://cloud-developer.weebly.com/form.html
	"""

	def __init__(self, form_id, user_id, site_id, data=None):
		self.user_id = int(user_id)
		self.site_id = int(site_id)
		self.form_id = int(form_id)
		self._endpoint = "user/{0}/site/{1}/form/{2}".format(
			self.user_id,
			self.site_id,
			self.form_id
		)
		CloudResource.__init__(self, data)

	def id(self):
		"""Return the form_id"""
		return self.form_id

	def list_form_entries(self, **filters):
		"""
		Returns a iterable of `FormEntry` resources for a given form subject to
		keyword argument filters.
		"""
		result = self.client.get(self._endpoint + "/entry", params=filters)
		return PaginatedList(
			result,
			FormEntry,
			(self.user_id, self.site_id, self.form_id),
			"form_entry_id"
		)

	def get_form_entry(self, form_entry_id):
		"""Return the `FormEntry` with the given id."""
		return FormEntry(form_entry_id, self.user_id, self.site_id, self.form_id)
