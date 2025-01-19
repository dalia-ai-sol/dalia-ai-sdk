
from modules.base.chat_element import Chat_Element

class Chat:

	def __init__(self, chat_config=None):
		self.chat_history = []
		self.current_chat_element = None
		self.last_chat_element_time = None

	def add_chat_element(self, chat_input):
		role = chat_input["role"]
		text = chat_input["text"]
		ce = Chat_Element(role, text)
		self.chat_history.append(ce)
		self.current_chat_element = ce
		self.last_chat_element_time = ce.time

	def get_current_chat_element_text(self):
		chat_text = self.current_chat_element.text
		return chat_text

	def get_history(self):
		with open("./prompts/chat/chat.txt") as txt_file:
			chat_text = txt_file.read()
		if len(self.chat_history) > 0:
			chat_gistory_text = ""
			for ce in self.chat_history:
				chat_elm_text = f"""
					{ce.role} said [at: {ce.time} UTC]:
					{ce.text}
				"""
				chat_gistory_text += chat_elm_text + "\n"
		else:
			chat_gistory_text = "No conversation has happened yet."
		chat_text += "\n" + chat_gistory_text
		return chat_text