import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

chat_history = []

while True:
    user_input = input("You > ")
    if user_input.lower() in ("exit", "quit"):
        print ("Mr. Chatter > Goodbye!")
        break
    
    chat_history.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model = "openai/gpt-oss-20b",
        messages = chat_history
    )
    bot_reply = response.choices[0].message.content 
    chat_history.append({"role": "assistant", "content": bot_reply}) 
    
    print (f"Mr. Chatter > {bot_reply}")