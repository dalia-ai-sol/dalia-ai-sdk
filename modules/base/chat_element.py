
import arrow

class Chat_Element:

	def __init__(self, role, text):
		self.role = role
		self.text = text
		self.time = arrow.utcnow().format("YYYY-MM-DD HH:mm:ss")
