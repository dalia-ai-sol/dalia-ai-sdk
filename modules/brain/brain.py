
from modules.base.chat import Chat
from modules.brain.planner import Planner
from modules.brain.persona import Persona
from modules.brain.actions import Actions
from modules.brain.short_term_memory import Short_Term_Memory

class Brain:

	def __init__(self, brain_config):
		# Brain modules
		self.chat = None
		self.planner = None
		self.persona = None
		self.actions = None
		self.short_term_memory = None
		self.planning_output = {}
		self.planning_output["general_conversation"] = "Action: Engage in general conversation"
		self.planning_output["generate_response_to_user"] = "Action: Create response to user"
		self.planning_output["get_token_analysis"] = "Action: Run analysis on token"
		self.planning_output["summary_of_actions"] = "Action: Generate summary of actions"


		self.mental_state = {
			"persona" : "",
			"chat_history" : "",
			"actions" : "",
			"short_term_memory" : "",
			"plan" : ""
		}
		# Wake up brain
		self.wakeup(brain_config)

	def wakeup(self, brain_config):
		self.chat = Chat()
		self.planner = Planner()
		self.persona = Persona(persona = brain_config["persona"])
		self.actions = Actions(brain_config["actions"])
		self.short_term_memory = Short_Term_Memory()
		self.initialize_mental_state()

	def process(self, input):
		if input["type"] == "chat":
			if input["action"] == "normal":
				result = self.think(input)
				return result
			else:
				raise ValueError("Action not supported.")
		else:
			raise ValueError("Input type not supported.")


	def think(self, input):
		self.update_chat(input["chat_data"])
		self.update_mental_state()
		self.mental_state = self.short_term_memory.forget(self.mental_state)

		reasoning_cyle = 0
		while True:
			next_plan = self.planner.plan_next_step(self.mental_state)
			if next_plan == "generate_response_to_user":
				response = self.actions.generate_response_to_user(self.mental_state)
				result = self.end_thinking(response)
				return response
			else:
				memory, memory_type = self.actions.perform_action(next_plan, self.mental_state)
				self.make_memories(memory, memory_type, next_plan)

			reasoning_cyle += 1
			if reasoning_cyle > 2:
				response = self.actions.generate_response_to_user(self.mental_state, max_reasoning_cycle=True)
				result = self.end_thinking(response)
				return response
	
	def end_thinking(self, response):
		chat_obj = {}
		chat_obj["role"] = "AI"
		chat_obj["text"] = response
		self.update_chat(chat_obj)
		self.update_mental_state()
		return chat_obj

	def make_memories(self, memory, memory_type, next_plan):
		self.mental_state = self.short_term_memory.update_short_term_memory(self.mental_state, memory, memory_type, next_plan)

	def update_chat(self, chat_obj):
		self.chat.add_chat_element(chat_obj)

	def update_mental_state(self):
		self.mental_state["chat_history"] = self.chat.get_history()

	def initialize_mental_state(self):
		# Grab state components:
		self.mental_state["persona"] = self.persona.get_persona()
		self.mental_state["chat_history"] = self.chat.get_history()
		self.mental_state["actions"] = self.actions.get_possible_actions()
		self.mental_state["short_term_memory"] = self.short_term_memory.get_short_term_memory()
		self.mental_state["plan"] = ""
		

