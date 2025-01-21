from modules.base.helper_functions import promptify_mental_state
from modules.toolbox.token.token_utils import *
from modules.toolbox.news.news import get_latest_news
from modules.base.llm import LLM
import json
import arrow

class Actions:

	def __init__(self, action_config=None):
		self.llm = LLM(llm_source="openai")
		self.actions = {}
		self.actions["summary_of_actions"] = self.summary_of_actions
		self.actions["general_conversation"] = self.general_conversation
		self.actions["generate_response_to_user"] = self.generate_response_to_user
		self.actions["get_token_analysis"] = self.get_token_analysis
		self.actions["compare_tokens"] = self.compare_tokens
		self.actions["is_it_good_time_to_buy"] = self.is_it_good_time_to_buy
		self.actions["get_latest_news_on_query"] = self.get_latest_news_on_query

	def get_possible_actions(self):
		with open("./prompts/actions/possible_actions.txt") as txt_file:
			possible_actions = txt_file.read()
		return possible_actions

	def perform_action(self, action_name, mental_state):
		memory, memory_type = self.actions[action_name](mental_state)
		return memory, memory_type

	def summary_of_actions(self, mental_state):
		with open("./prompts/actions/summarize_actions.txt") as txt_file:
			plan_instruction = txt_file.read()
		mental_state["plan"] = plan_instruction
		mental_state_prompt = promptify_mental_state(mental_state)
		system_prompt = mental_state_prompt
		user_prompt = "Please provide your response."
		result = self.llm.call(system_prompt, user_prompt, json_extract=False)
		result_type = "Response to User"
		return result, result_type

	def general_conversation(self, mental_state):
		with open("./prompts/actions/general_conversation.txt") as txt_file:
			plan_instruction = txt_file.read()
		mental_state["plan"] = plan_instruction
		mental_state_prompt = promptify_mental_state(mental_state)
		system_prompt = mental_state_prompt
		user_prompt = "Please provide your response."
		result = self.llm.call(system_prompt, user_prompt, json_extract=True)
		result = result["response_to_user"]
		result_type = "Response to User"
		return result, result_type
	
	def generate_response_to_user(self, mental_state, max_reasoning_cycle=False):
		with open("./prompts/actions/generate_response_to_user.txt") as txt_file:
			plan_instruction = txt_file.read()
		if max_reasoning_cycle:
			plan_instruction += """
				It has taken a lot of reasoning cycles to answer this question. Maybe the question is not answerable.
				Keep that in mind.
			"""
		mental_state["plan"] = plan_instruction
		mental_state_prompt = promptify_mental_state(mental_state)
		system_prompt = mental_state_prompt
		user_prompt = "Please provide your response."
		result = self.llm.call(system_prompt, user_prompt, json_extract=True)
		return result
	
	def get_token_analysis(self, mental_state):
		with open("./prompts/actions/token_analysis/get_token_address.txt") as txt_file:
			system_prompt = txt_file.read()
		chat_data = mental_state["chat_history"]
		system_prompt = system_prompt.replace("__CHAT__", str(chat_data))
		user_prompt = "Please provide your response."
		result = self.llm.call(system_prompt, user_prompt, json_extract=True)
		token_addresses = result["token_addresses"]
		if len(token_addresses) > 0:
			response = ""
			for token in token_addresses:
				token_metatadata = get_token_metadata(token)
				token_trade_info = get_token_trade_data(token)
				token_info = token_metatadata | token_trade_info
				with open("./prompts/actions/token_analysis/analysis.txt") as txt_file:
							system_prompt = txt_file.read()
				system_prompt = system_prompt.replace("__TOKEN_DATA__", json.dumps(token_info))
				user_prompt = "Please provide your response."
				result = self.llm.call(system_prompt, user_prompt, json_extract=False)
				response += f"""
					Analysis for token : {token}
					Analysis HTML :
					{result}
				"""
		else:
			response = "No token addresses found."
		result_type = "Response to User"
		return 	response, result_type
	
	def compare_tokens(self, mental_state):
		analysis_of_tokens = self.get_token_analysis(mental_state)
		with open("./prompts/actions/token_analysis/compare_tokens.txt") as txt_file:
			system_prompt = txt_file.read()
		system_prompt = system_prompt.replace("__DATA__", analysis_of_tokens)
		user_prompt = "Please provide your response."
		result = self.llm.call(system_prompt, user_prompt, json_extract=True)
		return result
	
	def is_it_good_time_to_buy(self, mental_state):
		with open("./prompts/actions/token_analysis/get_token_address.txt") as txt_file:
			system_prompt = txt_file.read()
		chat_data = mental_state["chat_history"]
		system_prompt = system_prompt.replace("__CHAT__", str(chat_data))
		user_prompt = "Please provide your response."
		result = self.llm.call(system_prompt, user_prompt, json_extract=True)
		token_addresses = result["token_addresses"][0]
		token_info = get_token_trade_data(token_addresses)
		time_now = arrow.utcnow().timestamp()
		time_past = arrow.utcnow().shift(hours=-1).timestamp()
		data = get_token_pricing_history(token_addresses, start_time=int(time_past), end_time=int(time_now), interval_type='1m')
		price_data = data[1]
		date_data = [arrow.get(i).to('utc').format("YYYY-MM-DD HH:mm:ss") for i in  data[0]]
		price_data = {"date time":date_data , "prices":price_data}
		with open("./prompts/actions/token_analysis/good_time_to_buy.txt") as txt_file:
			system_prompt = txt_file.read()
		system_prompt = system_prompt.replace("__STATS__", json.dumps(token_info))
		system_prompt = system_prompt.replace("__PRICE__", json.dumps(price_data))
		user_prompt = "Please provide your response."
		result = self.llm.call(system_prompt, user_prompt, json_extract=False)
		result_type = "Response to User"
		return result, result_type
	
	def get_latest_news_on_query(self, mental_state):
		with open("./prompts/actions/news_analysis/get_news_query_topic.txt") as txt_file:
			system_prompt = txt_file.read()
		chat_data = mental_state["chat_history"]
		system_prompt = system_prompt.replace("__CHAT__", str(chat_data))
		user_prompt = "Please provide your response."
		result = self.llm.call(system_prompt, user_prompt, json_extract=True)
		news_qeury = result["news_query"]
		news_data = get_latest_news(news_qeury)
		with open("./prompts/actions/news_analysis/analyze_news.txt") as txt_file:
			system_prompt = txt_file.read()
		system_prompt = system_prompt.replace("__NEWS_QUERY__", news_qeury)
		system_prompt = system_prompt.replace("__NEWS_DATA__", str(news_data))
		user_prompt = "Please provide your response."
		result = self.llm.call(system_prompt, user_prompt, json_extract=False)
		result_type = "Response to User"
		return result, result_type