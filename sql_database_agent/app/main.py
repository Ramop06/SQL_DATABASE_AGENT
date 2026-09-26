from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from app.agent import run_agent


app = FastAPI(
    title="SQL Database Agent"
)


class Question(BaseModel):
    question: str


HTML_PAGE = """
<!DOCTYPE html>

<html>

<head>

    <title>SQL Database Agent</title>

    <style>

        body {
            font-family: Arial, sans-serif;
            background: #f5f7fb;
            margin: 0;
            padding: 40px;
        }

        .container {
            max-width: 900px;
            margin: auto;
            background: white;
            padding: 35px;
            border-radius: 15px;
            box-shadow: 0 5px 25px rgba(0,0,0,0.1);
        }

        h1 {
            color: #1f2937;
        }

        .subtitle {
            color: #6b7280;
            margin-bottom: 30px;
        }

        input {
            width: 100%;
            padding: 15px;
            font-size: 16px;
            border: 1px solid #ddd;
            border-radius: 8px;
            box-sizing: border-box;
        }

        button {
            margin-top: 15px;
            padding: 13px 25px;
            background: #ef4444;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
        }

        button:hover {
            background: #dc2626;
        }

        #result {
            margin-top: 25px;
        }

        .sql {
            background: #111827;
            color: #f9fafb;
            padding: 15px;
            border-radius: 8px;
            white-space: pre-wrap;
        }

        .error {
            background: #fee2e2;
            color: #991b1b;
            padding: 15px;
            border-radius: 8px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }

        th, td {
            padding: 10px;
            border: 1px solid #ddd;
            text-align: left;
        }

        th {
            background: #f3f4f6;
        }

    </style>

</head>


<body>

<div class="container">

    <h1>🗄️ SQL Database Agent</h1>

    <div class="subtitle">
        Ask questions about your database in natural language.
    </div>

    <input
        id="question"
        placeholder="Example: show me top 5 CSE students by marks"
    >

    <button onclick="runAgent()">
        🔎 Run Agent
    </button>

    <div id="result"></div>

</div>


<script>

async function runAgent() {

    const question =
        document.getElementById("question").value;

    const result =
        document.getElementById("result");

    if (!question.trim()) {

        result.innerHTML =
            '<div class="error">Please enter a question.</div>';

        return;
    }

    result.innerHTML = "Thinking...";

    try {

        const response = await fetch(
            "/ask",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    question: question
                })
            }
        );

        const data = await response.json();

        if (!data.success) {

            result.innerHTML =
                `<div class="error">
                    ${data.error}
                </div>`;

            return;
        }

        let html = "";

        html += "<h3>Generated SQL</h3>";

        html +=
            `<div class="sql">${data.sql}</div>`;

        html += "<h3>Results</h3>";

        if (!data.results ||
            data.results.length === 0) {

            html += "<p>No records found.</p>";

        } else {

            html += "<table>";

            const columns =
                Object.keys(data.results[0]);

            html += "<tr>";

            columns.forEach(column => {

                html += `<th>${column}</th>`;

            });

            html += "</tr>";

            data.results.forEach(row => {

                html += "<tr>";

                columns.forEach(column => {

                    html +=
                        `<td>${row[column]}</td>`;

                });

                html += "</tr>";

            });

            html += "</table>";
        }

        result.innerHTML = html;

    } catch (error) {

        result.innerHTML =
            `<div class="error">
                ${error}
            </div>`;
    }
}

</script>

</body>

</html>
"""


@app.get("/", response_class=HTMLResponse)
def home():

    return HTML_PAGE


@app.post("/ask")
def ask_database(question: Question):

    return run_agent(
        question.question
    )