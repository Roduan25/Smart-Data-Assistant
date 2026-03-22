# 🏢 Enterprise Data Assistant (V3.0)

An intelligent, enterprise-grade project management and data analysis platform. This tool bridges the gap between static databases and natural language, allowing project managers and document controllers to interact with their live data using conversational AI.

## 🚀 Key Features

* **Live PostgreSQL Integration:** Bypasses static Excel files by connecting directly to a local PostgreSQL database, ensuring real-time data analysis and strict data governance.
* **Autonomous AI Agent (Gemini 1.5 Pro):** Employs an advanced reasoning AI agent that writes and executes Python code in the background to calculate precise metrics (e.g., total budgets, completion rates) before answering.
* **Automated Executive Reporting:** Generates comprehensive, professionally formatted executive summaries with a single click, ready for immediate download.
* **Dynamic Data Visualization:** Capable of understanding complex analytical requests and generating visual charts (Matplotlib/Seaborn) directly within the chat interface.
* **Offline Fallback Mode:** Supports traditional ingestion of multiple Excel/CSV files for legacy workflows.

## 🛠️ Technology Stack

* **Frontend:** Streamlit (Python)
* **Database Engine:** PostgreSQL, SQLAlchemy, Psycopg2
* **AI & LLM:** Google Gemini 1.5 Pro, LangChain (Experimental Agents)
* **Data Processing & Visualization:** Pandas, Matplotlib, Seaborn

## ⚙️ How It Works (The Agentic Workflow)

Unlike standard LLMs that "guess" answers based on language patterns, this application utilizes an Agentic Workflow:
1. **Understand:** The Agent parses the user's natural language query.
2. **Execute:** It translates the query into valid Python code (using `python_repl_ast`) and executes it against the live Pandas DataFrame securely.
3. **Analyze & Report:** It reads the exact numerical output and synthesizes it into a highly accurate, data-driven response or visual chart.

## 🛡️ Security & Privacy
Designed with enterprise data policies in mind. The PostgreSQL database runs locally, meaning sensitive project budgets and statuses never leave the host machine. Only the analytical logic and code generation are handled via the API, ensuring maximum data privacy.

---
*Built with passion to revolutionize digital records and project management.*