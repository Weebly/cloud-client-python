import json
import hmac
import base64
import hashlib

# Try getting Python requests module http://docs.python-requests.org/en/master/
try:
	import requests
except ImportError:
	raise ImportError("Requests module not available. Use 'pip install requests'.")

from .WeeblyCloudResponse import *

class CloudClient(object):
	"""The base API client for interfacing with the Weebly Cloud API"""

	BASE_API = "https://api.weeblycloud.com/"

	# API credentials
	API_KEY = None
	API_SECRET = None
	SESSION = None

	def __init__(self, api_key=None, api_secret=None):
		if api_key and api_secret:
			self.api_key = api_key
			self.api_secret = api_secret
		elif CloudClient.API_KEY and CloudClient.API_SECRET:
			self.api_key = CloudClient.API_KEY
			self.api_secret = CloudClient.API_SECRET
		else:
			raise RuntimeError("No API credentials provided.")

		if not CloudClient.SESSION:
			CloudClient.SESSION = requests.Session()
		self.session = CloudClient.SESSION

		self.session.headers.update({
			"Content-type": "application/json",
			"W-Cloud-Client-Type": "python",
			"W-Cloud-Client-Version": "1.0.0",
			'X-Public-Key': self.api_key
		})

	def get(self, endpoint, content=None, params=None, page_size=None, page=1):
		"""Make a GET call and return a WeeblyCloudResponse object"""
		params = params or {}
		content = content or {}

		if page_size:
			page_size = int(page_size)
			if page_size > 200 or page_size < 25:
				raise RuntimeError("Invalid page size.")
			params.update({"limit":page_size})
		if page is not 1:
			params.update({"page":page})
		return self._call("GET", endpoint, content, params)

	def post(self, endpoint, content=None, params=None):
		"""Make a POST call and return a WeeblyCloudResponse object"""
		return self._call("POST", endpoint, content, params)

	def patch(self, endpoint, content=None, params=None):
		"""Make a PATCH call and return a WeeblyCloudResponse object"""
		return self._call("PATCH", endpoint, content, params)

	def put(self, endpoint, content=None, params=None):
		"""Make a PUT call and return a WeeblyCloudResponse object"""
		return self._call("PUT", endpoint, content, params)

	def delete(self, endpoint, content=None, params=None):
		"""Make a DELETE call and return a WeeblyCloudResponse object"""
		return self._call("DELETE", endpoint, content, params)

	def __sign(self, request_type, endpoint, content=None):
		"""
		Signs a request and returns the HMAC hash.
		See https://cloud-developer.weebly.com/about-the-rest-apis.html#signing-and-authenticating-requests
		"""
		request = request_type + "\n" + endpoint + "\n" + content
		mac = hmac.new(self.api_secret.encode('utf-8'),
					   request.encode('utf-8'),
					   digestmod=hashlib.sha256).hexdigest()
		return base64.b64encode(mac.encode('utf-8'))

	def _call(self, method, endpoint, content=None, params=None):
		"""Make a call and return a WeeblyCloudResponse object"""
		params = params or {}
		content = content or {}

		json_data = json.dumps(content)
		endpoint = endpoint.strip("/")
		headers = {"X-Signed-Request-Hash": self.__sign(method, endpoint, json_data)}

		response = self.session.request(method=method,
										url=(CloudClient.BASE_API + endpoint),
										headers = headers,
										params=params,
										data = json_data)

		return WeeblyCloudResponse(self.session, response)
