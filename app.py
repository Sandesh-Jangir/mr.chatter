import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


while True:
    user_input = input("You > ")
    if user_input.lower() in ("exit", "quit"):
        print ("Mr. Chatter > Goodbye!")
        break
    
    response = client.chat.completions.create(
        model = "openai/gpt-oss-20b",
        messages = [{"role": "user", "content": user_input}]
    )
    bot_reply = response.choices[0].message.content  
    print (f"Mr. Chatter > {bot_reply}")
