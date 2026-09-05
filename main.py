from agent import ask_agent
import database

database.init_db()

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit"]:
            break
        reply = ask_agent(user_input)
        print(f"Agent: {reply}")