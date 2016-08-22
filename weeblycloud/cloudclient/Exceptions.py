class ResponseError(RuntimeError):
	"""Exception used when there is an error in Weebly's API response"""
	def __init__(self, error_message, error_code):
		self.code = error_code
		self.message = error_message
		the_message = "(CODE: #{0}) {1}".format(str(error_code), error_message)
		RuntimeError.__init__(self,the_message)

class PaginationError(TypeError):
	"""Exception used when there is an error involving pagination"""
	pass
