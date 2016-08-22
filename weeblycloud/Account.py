from .SaveableResource import *
from .PaginatedList import *
from .Plan import *
from .User import *

class Account(SaveableResource):
	"""
	Represents an Account resource.
	https://cloud-developer.weebly.com/account.html
	"""

	def __init__(self):
		self._endpoint = "account"
		SaveableResource.__init__(self)

	def _get(self):
		response = self.client.get(self._endpoint)
		self.properties = response.json['account']

	def create_user(self, email, **properties):
		"""
		Creates a `User`. Requires the user's **email**, and optionally accepts
		keyword arguments of additional properties. Returns a `User` resource
		on success.
		"""
		properties.update({"email":email})
		response = self.client.post("user",content=properties)
		return User(response.json['user']['user_id'])

	def get_user(self, user_id):
		"""Get a user with a given ID"""
		return User(user_id)

	def list_plans(self):
		"""
		Returns a iterable of all Plan resources.
		"""
		result = self.client.get("plan")
		result.json = Plan.normalize_plan_list(result.json)
		return PaginatedList(result, Plan, (), "plan_id")

	def get_plan(self, plan_id):
		"""
		Return the Plan with the given ID.
		"""
		return Plan(plan_id)
