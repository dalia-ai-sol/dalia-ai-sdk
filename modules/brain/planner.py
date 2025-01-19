
from modules.base.helper_functions import promptify_mental_state
from modules.base.llm import LLM

class Planner:

	def __init__(self, planner_config=None):
		self.llm = LLM(llm_source="openai")


	def plan_next_step(self, mental_state):
		with open("./prompts/planner/next_step_planning.txt") as txt_file:
			plan_instruction = txt_file.read()
		mental_state["plan"] = plan_instruction
		mental_state_prompt = promptify_mental_state(mental_state)
		system_prompt = mental_state_prompt
		user_prompt = "Please provide your response."
		next_step = self.llm.call(system_prompt, user_prompt, json_extract=True)
		return next_step["next_step"]