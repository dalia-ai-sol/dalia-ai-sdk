class Short_Term_Memory:

	def __init__(self):
		pass

	def get_short_term_memory(self):
		with open("./prompts/short_term_memory/short_term_memory.txt") as txt_file:
			short_term_memory = txt_file.read()
		return short_term_memory
	
	def forget(self, mental_state):
		mental_state["short_term_memory"] = self.get_short_term_memory()
		return mental_state

	def update_short_term_memory(self, mental_state, memory, memory_type, next_plan):
		make_memory = f"""
			# Memory:
			Action taken: {next_plan}
			Memory type: {memory_type}
			Memory value: {memory}
		"""
		mental_state["short_term_memory"] += "\n" + make_memory
		return mental_state