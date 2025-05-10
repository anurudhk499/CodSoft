responses = {
    "hi": "Hello! How can I help you?",
    "hello": "Hi there! How can I assist you?",
    "how are you?": "I'm just a program, but I'm functioning perfectly!",
    "what is your name?": "I'm a rule-based chatbot created for learning.",
    "bye": "Goodbye! Have a nice day!"
}
def chatbot_response(user_input):
    user_input = user_input.lower()  # Convert to lowercase for case-insensitive matching
    return responses.get(user_input, "I'm sorry, I don't understand that.")
print("Chatbot: Hello! Start chatting with me. Type 'bye' to end the conversation.")

while True:
    user_input = input("You: ")
    if user_input.lower() == "bye":
        print("Chatbot: Goodbye! Have a great day!")
        break
    response = chatbot_response(user_input)
    print("Chatbot:", response)
    import re

def chatbot_response(user_input):
    user_input = user_input.lower()
    
    if re.search(r"\b(name)\b", user_input):
        return "I'm a simple rule-based chatbot."
    elif re.search(r"\b(time)\b", user_input):
        from datetime import datetime
        return f"The current time is {datetime.now().strftime('%H:%M:%S')}."
    elif user_input in responses:
        return responses[user_input]
    else:
        return "I'm sorry, I don't understand that."
