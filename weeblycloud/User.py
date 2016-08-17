from .SaveableResource import *
from .PaginatedList import *
from .Theme import *
from .Site import *

class User(SaveableResource):
	"""
	Represents a User resource.
	https://cloud-developer.weebly.com/user.html
	"""

	def __init__(self, user_id, data=None):
		self.user_id = int(user_id)
		self._endpoint = "user/{0}".format(self.user_id)
		SaveableResource.__init__(self, data)

	def _get(self):
		response = self.client.get(self._endpoint)
		self.properties = response.json["user"]

	def id(self):
		"""Returns the ID"""
		return self.user_id

	def enable(self):
		"""
		Enables a user account after an account has been disabled.
		Enabling a user account will allow users to log into the editor.
		When a user is created, their account is automatically enabled.
		"""
		result = self.client.post(self._endpoint + "/enable")
		return bool(result.json["success"])

	def disable(self):
		"""
		Disables a user account. When a user account is disabled, the user will
		no longer be able to log into the editor. If an attempt to create a login
		link is made on a disabled account, an error is thrown.
		"""
		result = self.client.post(self._endpoint + "/disable")
		return bool(result.json["success"])

	def login_link(self):
		"""
		Generates a one-time link that will direct users to the editor for
		the last site that was modified in the account. This method requires
		that the account is enabled and that the account has at least one site.
		"""
		result = self.client.post(self._endpoint + "/loginLink")
		return result.json["link"]

	def list_themes(self, **filters):
		"""
		Returns a iterable of `Theme` resources for a given user subject to
		keyword argument filters.
		"""
		result = self.client.get(self._endpoint + "/theme", params=filters)
		return PaginatedList(result, Theme, (self.user_id,), "theme_id")

	def create_theme(self, name, zip_url):
		"""
		Creates a Theme with name. Requires a zip_url and returns
		a Theme object.
		"""
		data = {"theme_name":name,"theme_zip":zip_url}
		response = self.client.post(self._endpoint + "/theme",content=data)
		return Theme(response.json['theme_id'], self.user_id)

	def list_sites(self, **filters):
		"""
		Returns a iterable of `Site` resources for a given user subject to
		keyword argument filters.
		"""
		result = self.client.get(self._endpoint + "/site", params=filters)
		return PaginatedList(result, Site, (self.user_id,), "site_id")

	def create_site(self, domain, **properties):
		"""
		Creates a `Site`. Requires the site's **domain** and optionally accepts
		keyword arguments of additional properties. Returns a `User` resource.
		"""
		properties.update({"domain":domain})
		response = self.client.post(self._endpoint + "/site",content=properties)
		return Site(response.json["site"]["site_id"], self.user_id, data=response.json["site"])

	def get_site(self, site_id):
		"""
		Return the Site with the given ID.
		"""
		return Site(site_id, self.user_id)
