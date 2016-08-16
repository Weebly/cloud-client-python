from .SaveableResource import *
from .Deleteable import *

class BlogPost(SaveableResource, Deleteable):
	"""
	Represents a BlogPost resource.
	https://cloud-developer.weebly.com/blog-post.html
	"""

	def __init__(self, blog_post_id, user_id, site_id, blog_id, data=None):
		self.user_id = int(user_id)
		self.site_id = int(site_id)
		self.blog_id = int(blog_id)
		self.blog_post_id = int(blog_post_id)
		self._endpoint = "user/{0}/site/{1}/blog/{2}/post/{3}".format(self.user_id, self.site_id, self.blog_id, self.blog_post_id)
		SaveableResource.__init__(self, data)

	def id(self):
		"""Returns the blog_post_id"""
		return self.blog_post_id
