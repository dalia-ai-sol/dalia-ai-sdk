def promptify_mental_state(mental_state):
	mental_state_prompt = ""
	for state in mental_state:
		mental_state_prompt += mental_state[state] + "\n"
	return mental_state_prompt