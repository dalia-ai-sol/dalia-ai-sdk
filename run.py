from dotenv import load_dotenv
load_dotenv()
from modules.brain.brain import Brain

with open("./welcome.txt") as txt_file:
	welcome_text = txt_file.read()

def main():
	print(welcome_text)
	brain_config = {
		"persona" : "crypto_expert",
		"actions" : ""
	}
	brain = Brain(brain_config)
	while True:
		# Get input from the user
		user_input = input("User >>>")
		# Exit condition
		if user_input.lower() in {"exit", "quit"}:
			print("Goodbye!")
			break
		brain_input = { 
			"type" : "chat",
			"action" : "normal",
			"chat_data" : {
				"role" : "user",
				"text" : user_input
			}
		}
		result = brain.process(brain_input)
		print("\n")
		print("Dalia AI >>>")
		for response in result["response"]:
			print(response)
		print("\n")

if __name__ == "__main__":
	main()