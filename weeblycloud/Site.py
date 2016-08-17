from .SaveableResource import *
from .Deleteable import *
from .PaginatedList import *
from .Plan import *
from .Page import *
from .Member import *
from .Group import *
from .Form import *
from .Blog import *

class Site(SaveableResource, Deleteable):
	"""
	Represents a Site resource.
	https://cloud-developer.weebly.com/site.html
	"""

	def __init__(self, site_id, user_id, data=None):
		self.user_id = int(user_id)
		self.site_id = int(site_id)
		self._endpoint = "user/{0}/site/{1}".format(self.user_id, self.site_id)
		SaveableResource.__init__(self, data)

	def _get(self):
		response = self.client.get(self._endpoint)
		self.properties = response.json["site"]

	def id(self):
		"""Return the site_id"""
		return self.site_id

	def publish(self):
		"""Publish the site"""
		response = self.client.post(self._endpoint + "/publish")
		return bool(response.json["success"])

	def unpublish(self):
		"""Unpublish the site"""
		response = self.client.post(self._endpoint + "/unpublish")
		return bool(response.json["success"])

	def login_link(self):
		"""
		Generates a one-time link that will direct users to the site specified.
		This method requires that the account is enabled.
		"""
		response = self.client.post(self._endpoint + "/loginLink")
		return response.json["link"]

	def set_publish_credentials(self, **options):
		"""
		Sets publish credentials for a given site to a dictionary, **data**.
		If a user's site will not be hosted by Weebly, publish credentials can
		be provided.  When these values are set, the site will be published to
		the location specified.
		"""
		response = self.client.post(self._endpoint + "/setPublishCredentials",
									content=options)
		return bool(response.json["success"])

	def restore(self, url):
		"""
		When a site is restored the owner of the site is granted access to it
		in the exact state it was when it was deleted, including the Weebly plan
		assigned. Restoring a site does not issue an automatic publish
		"""
		data = {"domain":url}
		response = self.client.post(self._endpoint + "/restore", content=data)
		return bool(response.json["success"])

	def disable(self):
		"""
		Suspends access to the given user's site in the editor by setting the
		suspended parameter to true. If a user attempts to access the site in
		the editor, an error is thrown.
		"""
		response = self.client.post(self._endpoint + "/disable")
		return bool(response.json["success"])

	def enable(self):
		"""
		Re-enables a suspended site by setting the suspended parameter to false.
		Users can access the editor for the site. Sites are enabled by default
		when created.
		"""
		response = self.client.post(self._endpoint + "/enable")
		return bool(response.json["success"])

	def get_plan(self):
		"""Returns the Plan resource for the site."""
		response = self.client.get(self._endpoint + "/plan")
		plan = response.json['plans']
		plan = list(plan.items())[0][1]
		return Plan(plan['plan_id'],data=plan)

	def set_plan(self, plan_id, term=None):
		"""
		Sets the site's plan to **plan_id** with an optional **term** length.
		If no term is provided the Weebly Cloud default is used (check API
		documentation).
		"""
		data = {"plan_id":plan_id}
		if term:
			data.update({"term":term})
		response = self.client.post(self._endpoint + "/plan", content=data)
		return bool(response.json["success"])

	def set_theme(self, theme_id, is_custom):
		"""
		Sets the site's theme to **theme_id**. Requires a parameter **is_custom**,
		distinguishing whether the theme is a Weebly theme or a custom theme.
		"""
		data = {"theme_id": theme_id, "is_custom":is_custom}
		response = self.client.post(self._endpoint + "/theme", content=data)
		return bool(response.json["success"])

	def list_pages(self, **filters):
		"""
		Returns a iterable of `Page` resources for a given site subject to
		keyword argument filters.
		"""
		result = self.client.get(self._endpoint + "/page", params=filters)
		return PaginatedList(result, Page, (self.user_id, self.site_id), "page_id")

	def list_members(self, **filters):
		"""
		Returns a iterable of `Member` resources for a given site subject to
		keyword argument filters.
		"""
		result = self.client.get(self._endpoint + "/member", params=filters)
		return PaginatedList(result, Member, (self.user_id, self.site_id), "member_id")

	def create_member(self, email, name, password, **properties):
		"""
		Creates a `Member`. Requires the member's **email**, **name**,
		**password**, and optionally accepts keyword arguments of additional
		properties. Returns a `Member` resource.
		"""
		properties.update({"email":email, "name":name, "password":password})
		response = self.client.post(self._endpoint + "/member",content=properties)
		return Member(response.json['member_id'],
					  self.user_id,
					  self.site_id,
					  data=response.json)

	def list_groups(self, **filters):
		"""
		Returns a iterable of `Group` resources for a given site subject to
		keyword argument filters.
		"""
		result = self.client.get(self._endpoint + "/group", params=filters)
		return PaginatedList(result, Group, (self.user_id, self.site_id), "group_id")

	def create_group(self, name):
		"""
		Creates a `Group`. Requires the group's **name**. Returns a `Group` resource.
		"""
		data = {"name":name}
		response = self.client.post(self._endpoint + "/group", content=data)
		return Group(response.json['group_id'],
					 self.user_id,
					 self.site_id,
					 data=response.json)

	def list_forms(self, **filters):
		"""
		Returns a iterable of `Form` resources for a given site subject to
		keyword argument filters.
		"""
		result = self.client.get(self._endpoint + "/form", params=filters)
		return PaginatedList(result, Form, (self.user_id, self.site_id), "form_id")

	def list_blogs(self, **filters):
		"""
		Returns a iterable of `Blog` resources for a given site subject to
		keyword argument filters.
		"""
		result = self.client.get(self._endpoint + "/blog", params=filters)
		return PaginatedList(result, Blog, (self.user_id, self.site_id), "blog_id")

	def get_page(self, page_id):
		"""Return the `Page` with the given id."""
		return Page(page_id, self.user_id, self.site_id)

	def get_member(self, member_id):
		"""Return the `Member` with the given id."""
		return Member(member_id, self.user_id, self.site_id)

	def get_group(self, group_id):
		"""Return the `Group` with the given id."""
		return Group(group_id, self.user_id, self.site_id)

	def get_form(self, form_id):
		"""Return the `Form` with the given id."""
		return Form(form_id, self.user_id, self.site_id)

	def get_blog(self, blog_id):
		"""Return the `Blog` with the given id."""
		return Blog(blog_id, self.user_id, self.site_id)
