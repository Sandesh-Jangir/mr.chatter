import os
import json
from groq import Groq
from chat_tools import search_web

tools = [
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the internet for current or factual information not known to the assistant, such as recent events, live data, or specific facts.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    }
                },
                "required": ["query"]
            }
        }
    }
]

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

chat_history = []

while True:
    user_input = input("You > ")
    if user_input.lower() in ("exit", "quit"):
        print("Mr. Chatter > Goodbye!")
        break

    chat_history.append({"role": "user", "content": user_input})

    # Inner loop: keep going until the model gives a plain text answer
    while True:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=chat_history,
            tools=tools
        )

        response_message = response.choices[0].message

        if response_message.tool_calls:
            chat_history.append({
                "role": "assistant",
                "content": response_message.content,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in response_message.tool_calls
                ]
            })

            for tool_call in response_message.tool_calls:
                if tool_call.function.name == "search_web":
                    args = json.loads(tool_call.function.arguments)
                    query = args["query"]

                    print(f"searching for {query}")
                    search_results = search_web(query)

                    chat_history.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": search_results
                    })
            # loop again so the model can respond to the search results
            continue
        else:
            bot_reply = response_message.content
            chat_history.append({"role": "assistant", "content": bot_reply})
            print(f"Mr. Chatter > {bot_reply}")
            break