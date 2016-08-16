from .CloudResource import *

class Page(CloudResource):
	"""
	Represents a Page resource.
	https://cloud-developer.weebly.com/page.html
	"""

	def __init__(self, page_id, user_id, site_id, data=None):
		self.user_id = int(user_id)
		self.site_id = int(site_id)
		self.page_id = int(page_id)
		self._endpoint = "user/{0}/site/{1}/page/{2}".format(self.user_id, self.site_id, self.page_id)
		CloudResource.__init__(self, data)

	def change_title(self, title):
		"""Change the page title"""
		data = {"title":title}
		response = self.client.patch(self._endpoint, content=data)
		if response.json['title'] is title:
			return True
		return False

	def id(self):
		"""Return the page_id"""
		return self.page_id
