
import json
from openai import OpenAI
from anthropic import Anthropic
from json_repair import repair_json


class LLM:

	def __init__(self, llm_source="openai"):
		self.llm_source = llm_source
		self.client = {}
		self.client["anthropic"] = Anthropic()
		self.client["openai"] = OpenAI()
		self.model = {}
		self.model["anthropic"] = "claude-3-haiku-20240307"
		self.model["openai"] = "gpt-4o-mini"
		self.llm_call = {}
		self.llm_call["anthropic"] = self.call_anthropic
		self.llm_call["openai"] = self.call_openai


	def call(self, system_prompt, user_prompt, json_extract=True):
		response = self.llm_call[self.llm_source](system_prompt, user_prompt, json_extract)
		return response


	def call_anthropic(self, system_prompt, user_prompt, json_extract):
		response = self.client[self.llm_source].messages.create(
			model = self.model[self.llm_source],
			max_tokens = 2048,
			temperature = 0,
			system=[
			{
				"type": "text", 
				"text": system_prompt,
			}
			],
			messages=[{"role": "user", "content": user_prompt}],
		)
		response = json.loads(response.to_json())
		if json_extract:
			content = self.extract_json(response["content"][0]["text"])
		else:
			content = response["content"][0]["text"]
		return content
	
	def call_openai(self, system_prompt, user_prompt, json_extract):
		response = self.client[self.llm_source].chat.completions.create(
			model = self.model[self.llm_source],
			temperature = 0,
			messages=[
				{"role": "system", "content":system_prompt},
				{"role": "user", "content":user_prompt}
			]
		)
		if json_extract:
			content = self.extract_json(response.choices[0].message.content)
		else:
			content = response.choices[0].message.content
		return content


	def extract_json(self, response):
		response = response.strip()
		response = response.replace("\n", "")
		json_start = response.index("{")
		json_end = response.rfind("}")
		repaired_json = repair_json(response[json_start : json_end + 1])
		return json.loads(repaired_json)