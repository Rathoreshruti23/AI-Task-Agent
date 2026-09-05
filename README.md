#  AI Task Agent

An autonomous task-management assistant built from scratch in Python, powered by Google's Gemini API. It understands natural language, extracts structured tasks, saves them permanently, and reasons over your task list to answer real questions — not just a chatbot with a to-do list bolted on.

Available as both a **command-line tool** and a **web app** (Streamlit), sharing the same underlying agent logic.



##  Features

- **Natural language task extraction** — just say what you need to do, in plain English, and the agent extracts the title, priority, and deadline on its own (no rigid commands like `add "task"`)
  > *"I need to finish the report by Friday, it's pretty urgent"* → saved as a structured task automatically
- **Persistent memory** — tasks are stored in a real SQLite database and survive across sessions, restarts, and reboots. Close everything, come back a week later — your tasks are still there.
- **Tool-calling / function-calling architecture** — the LLM doesn't just talk, it decides *when* to call real functions (`add_task`, `get_tasks`) based on what the user is asking
- **Genuine reasoning, not static output** — ask "what are my *urgent* tasks?" and the agent filters and reasons over the real data to answer exactly what was asked, rather than dumping the entire list
- **Dual interface** — a terminal (CLI) version for quick use, and a Streamlit web app with a chat UI for a more polished, demoable experience
- **Clean architecture** — agent logic, database logic, and interface (CLI/web) are fully separated into different files, so both interfaces share one consistent "brain"
- **Secure by design** — API key is never hardcoded; it's loaded from a `.env` file that's excluded from version control



##  How It Works (Architecture)

┌─────────────┐     ┌─────────────┐
│   main.py   │     │   app.py    │   ← two interfaces (CLI / Web)
│    (CLI)    │     │ (Streamlit) │
└──────┬──────┘     └──────┬──────┘
       │                   │
       └─────────┬─────────┘
                  ▼
           ┌─────────────┐
           │  agent.py   │   ← the "brain": talks to Gemini,
           │             │      decides when to call tools,
           └──────┬──────┘      reasons over results
                  ▼
           ┌─────────────┐
           │ database.py │   ← SQLite persistence layer
           │  (tasks.db) │
           └─────────────┘


**The reasoning loop** (what makes this an *agent*, not just a chatbot):
1. User sends a message (e.g., "what are my urgent tasks?")
2. Gemini decides whether to call a tool (`add_task` or `get_tasks`) based on intent
3. The tool runs against the real SQLite database
4. The **result is sent back to Gemini** for a second pass, so it can reason over the actual data
5. Gemini returns a natural, filtered, context-aware answer — not a canned response



## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python |
| LLM | Google Gemini API (`google-genai`) |
| Tool/function calling | Gemini native function calling |
| Database | SQLite (built-in, file-based) |
| Web UI | Streamlit |
| Secrets management | `python-dotenv` |



##  Project Structure


task-agent/
├── agent.py          # Core agent logic: LLM calls, tool definitions, reasoning
├── database.py        # SQLite persistence layer (add/get/delete tasks)
├── main.py            # CLI interface
├── app.py              # Streamlit web interface
├── requirements.txt    # Python dependencies
├── .env                # API key (excluded from Git)
├── .gitignore
└── tasks.db             # Auto-created on first run (excluded from Git)



##  Getting Started

# 1. Clone the repo
git clone https://github.com/YOUR-USERNAME/ai-task-agent.git
cd ai-task-agent

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\Activate.ps1      # Windows PowerShell
# source venv/bin/activate     # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your Gemini API key
echo "GEMINI_API_KEY=your_key_here" > .env
# Get a free key at https://aistudio.google.com

# 5. Run it — pick one:
python main.py              # CLI version
streamlit run app.py        # Web version


The SQLite database (`tasks.db`) is created automatically on first run — no manual setup required.


##  Example Interaction


You: I need to finish the report by Friday, it's pretty urgent
Agent: Got it — I've added 'Finish the report' to your tasks.

You: Add "Prepare for Java interview" to my tasks. It is high priority.
Agent: Got it — I've added 'Prepare for Java interview' to your tasks.

You: What are my urgent tasks?
Agent: Here are your high-priority tasks:
1. Finish the report
2. Prepare for Java interview
(Note: you also have "Submit project documentation" marked Medium priority, due Monday.)



##  Design Notes

- **Why SQLite, not a full database server?** For a personal-scale project like this, SQLite is the right tool — zero setup, file-based, and genuinely used in production for small-to-medium apps. No need for the overhead of running a separate database server.
- **Conversation vs. task persistence:** Task data is fully persistent across sessions (stored in `tasks.db`). Conversation history, however, currently only lasts for the duration of a single run — closing the terminal or refreshing the browser resets the chat, though all saved tasks remain untouched. This distinction between *application state* and *session state* was an intentional design checkpoint before adding full conversation persistence.



##  Why I Built This

To understand how modern AI agents actually work under the hood — going beyond prompting a chatbot, into the mechanics of tool/function calling, persistent memory, and multi-turn reasoning loops — by building the whole system from scratch rather than relying on a pre-built agent framework.
