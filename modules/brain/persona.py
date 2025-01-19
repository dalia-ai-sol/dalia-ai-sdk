class Persona:

	def __init__(self, persona=None):
		self.persona = persona
	
	def get_persona(self):
		with open(f"./prompts/personas/{self.persona}.txt") as txt_file:
			persona_text = txt_file.read()
		return persona_text