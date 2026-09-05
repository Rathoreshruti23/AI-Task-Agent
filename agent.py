import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import database

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# --- Tool definitions ---
add_task_function = {
    "name": "add_task",
    "description": "Add a new task to the user's task list",
    "parameters": {
        "type": "object",
        "properties": {
            "title": {"type": "string", "description": "Short description of the task"},
            "deadline": {"type": "string", "description": "Deadline in YYYY-MM-DD format, or empty if none"},
            "priority": {"type": "string", "enum": ["low", "medium", "high"]}
        },
        "required": ["title", "priority"]
    }
}

get_tasks_function = {
    "name": "get_tasks",
    "description": "Retrieve the user's current list of tasks",
    "parameters": {
        "type": "object",
        "properties": {}
    }
}

tools = types.Tool(function_declarations=[add_task_function, get_tasks_function])
config = types.GenerateContentConfig(
    system_instruction=(
        "You are a task management assistant. When the user mentions something "
        "they need to do, extract it as a task using the add_task tool. When they "
        "ask about their tasks (e.g. urgent, high priority, upcoming, all), use the "
        "get_tasks tool to retrieve the full list, then filter/reason over it "
        "yourself to answer exactly what they asked."
    ),
    tools=[tools]
)


def ask_agent(user_message):
    # First turn: send the user's message
    contents = [
        types.Content(role="user", parts=[types.Part(text=user_message)])
    ]

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=contents,
        config=config
    )

    part = response.candidates[0].content.parts[0]

    # If no tool call, just return the text directly
    if not part.function_call:
        return response.text

    fn = part.function_call

    # --- Run the actual tool ---
    if fn.name == "add_task":
        database.add_task(**fn.args)
        result = {"status": "success", "title": fn.args["title"]}
    elif fn.name == "get_tasks":
        tasks = database.get_all_tasks()
        result = {
            "tasks": [
                {"id": t[0], "title": t[1], "deadline": t[2], "priority": t[3]}
                for t in tasks
            ]
        }
    else:
        result = {"error": "unknown function"}

    # --- Send the tool result back to the model for a second pass ---
    contents.append(response.candidates[0].content)  # the model's function-call turn
    contents.append(
        types.Content(
            role="user",
            parts=[
                types.Part.from_function_response(
                    name=fn.name,
                    response=result
                )
            ]
        )
    )

    final_response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=contents,
        config=config
    )

    return final_response.text