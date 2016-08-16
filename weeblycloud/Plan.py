from .CloudResource import *

class Plan(CloudResource):
	"""
	Represents a Plan resource.
	https://cloud-developer.weebly.com/plan.html
	"""

	def __init__(self, plan_id, data=None):
		self.plan_id = int(plan_id)
		self._endpoint = "plan/{0}".format(self.plan_id)
		CloudResource.__init__(self, data)

	def _get(self):
		response = self.client.get(self._endpoint)
		plan = response.json['plans']

		# Plan has a weird return format
		self.properties = plan.itervalues().next()

	def id(self):
		"""Return the plan_id"""
		return self.plan_id

	@staticmethod
	def normalize_plan_list(plan_list):
		"""Fixes the weird list response of the plan endpoint."""
		plans = plan_list['plans']
		return list(plans.values())
