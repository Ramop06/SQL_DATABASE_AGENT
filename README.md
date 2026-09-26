# 🤖 SQL Database Agent

> **An AI-powered database assistant that converts natural-language questions into SQL queries, executes them safely on a SQLite database, and returns the results through an interactive interface.**

Built with **Python, FastAPI, SQLite, Streamlit, and LLM-based query generation**.


🚀 Features

* 💬 Ask database questions using natural language
* 🧠 Convert natural-language questions into SQL queries
* 🗄️ Execute generated SQL against a SQLite database
* 📊 Return database results in a readable format
* ⚡ FastAPI backend for API-based interaction
* 🎨 Streamlit interface for interactive usage
* 🔒 Environment variables for sensitive configuration
* 🧩 Modular agent, database, configuration, and API components



🏗️ Architecture

         User
          │
          ▼
     Streamlit UI
          │
          ▼
      SQL Agent
          │
  Understands natural-language question
          │
    Generates SQL query
          │
          ▼
     Database Layer
          │   
          ▼
    SQLite Database
          │
          ▼
     Query Results
          │
          ▼
Streamlit / API Response


 📁 Project Structure

SQL_DATABASE_AGENT/
│
├── app/
│   ├── __init__.py
│   ├── agent.py
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   └── streamlit_app.py
│
├── create_database.py
├── requirements.txt
├── README.md
└── .gitignore


 🛠️ Tech Stack

| Technology   | Purpose                           |
| ------------ | --------------------------------- |
| Python       | Core application                  |
| FastAPI      | Backend API                       |
| SQLite       | Database                          |
| Streamlit    | Interactive UI                    |
| LLM          | Natural-language → SQL generation |
| Git & GitHub | Version control                   |


 ⚙️ **Installation**

 **1. Clone the repository**

git clone https://github.com/Ramop06/SQL_DATABASE_AGENT.git
cd SQL_DATABASE_AGENT


 **2. Create a virtual environment** 

python -m venv .venv


 **3. Activate the virtual environment**

 Windows

powershell
.venv\Scripts\activate


 macOS / Linux

source .venv/bin/activate


 **4. Install dependencies**

pip install -r requirements.txt




 🗄️ **Create the Database**

Run:

python create_database.py


This creates the SQLite database used by the application.



 ▶️ **Run the Application**

 **Streamlit**

streamlit run app/streamlit_app.py


Then open the local URL displayed by Streamlit.

 **FastAPI**

uvicorn app.main:app --reload

The API can then be accessed through the local FastAPI server.


## 💡 Example Queries

The agent can handle questions such as:

Show all students.

How many students are in the database?

Show students with a CGPA greater than 8.

Which student has the highest CGPA?

The system converts the natural-language request into an SQL query, executes it, and returns the result.


## 🧠 How It Works

1. User enters a question in natural language.
2. The SQL agent interprets the question.
3. An SQL query is generated.
4. The database layer executes the query.
5. The result is returned to the user.
6. Streamlit displays the result interactively.


## 🔐 Environment Variables

If your application uses an API key, create a `.env` file:

API_KEY=your_api_key_here


**Never commit API keys, passwords, or other secrets to GitHub.**

The `.env` file should be included in `.gitignore`.


## 🎯 Project Goals

This project demonstrates practical experience with:

* LLM application development
* AI agents
* Natural-language-to-SQL systems
* API development
* Database interaction
* Python backend development
* Streamlit application development
* Git/GitHub workflows


## 🔮 Future Improvements

> Add SQL query validation
> Add conversation memory
> Add multiple database support
> Add PostgreSQL/MySQL support
> Add authentication
> Add query history
> Add SQL explanation
> Add charts and visualizations
> Add automated tests
> Add Docker deployment
> Add agent/tool-calling workflow


## 👨‍💻 Author

**Ramop06**

GitHub: https://github.com/Ramop06


## ⭐ If you find this project useful

Consider giving the repository a ⭐ on GitHub.

