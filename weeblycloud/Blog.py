from .CloudResource import *
from .PaginatedList import *
from .BlogPost import *

class Blog(CloudResource):
	"""
	Represents a Blog resource.
	https://cloud-developer.weebly.com/blog.html
	"""

	def __init__(self, blog_id, user_id, site_id, data=None):
		self.user_id = int(user_id)
		self.site_id = int(site_id)
		self.blog_id = int(blog_id)
		self._endpoint = "user/{0}/site/{1}/blog/{2}".format(self.user_id, self.site_id, self.blog_id)
		CloudResource.__init__(self, data)

	def id(self):
		"""Returns the blog_id"""
		return self.blog_id

	def list_blog_posts(self, **filters):
		"""
		Returns a iterable of `BlogPost` resources for a given blog subject to
		keyword argument filters.
		"""
		result = self.client.get(self._endpoint + "/post", params=filters)
		return PaginatedList(result, BlogPost, (self.user_id, self.site_id, self.blog_id), "post_id")

	def create_blog_post(self, post_body, **properties):
		"""
		Creates a `BlogPost`. Requires the post's **body** and optionally
		accepts keyword arguments of additional properties. Returns a
		`BlogPost` resource.
		"""
		properties.update({"post_body":post_body})
		response = self.client.post(self._endpoint + "/post",content=properties)
		return BlogPost(response.json['post_id'], self.user_id, self.site_id, self.blog_id, data=response.json)

	def get_blog_post(self, blog_post_id):
		"""Return the `BlogPost` with the given id."""
		return BlogPost(blog_post_id, self.user_id, self.site_id, self.blog_id)
