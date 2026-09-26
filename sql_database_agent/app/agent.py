import re

from groq import Groq

from app.config import GROQ_API_KEY, MODEL_NAME
from app.database import get_schema, execute_sql


# Create Groq client
client = Groq(
    api_key=GROQ_API_KEY
)


def clean_sql(sql: str) -> str:
    """
    Remove markdown code fences if the model returns them.
    """

    sql = sql.strip()

    sql = re.sub(
        r"^```sql\s*",
        "",
        sql,
        flags=re.IGNORECASE
    )

    sql = re.sub(
        r"^```\s*",
        "",
        sql
    )

    sql = re.sub(
        r"\s*```$",
        "",
        sql
    )

    return sql.strip()


def generate_sql(question: str, schema: str) -> str:

    system_prompt = f"""
You are an expert SQLite SQL assistant.

Your job is to convert a user's natural-language question
into ONE valid SQLite SELECT query.

DATABASE SCHEMA:
{schema}

RULES:

1. Generate ONLY SQL.
2. Do not use markdown.
3. Do not explain the SQL.
4. Only generate SELECT queries.
5. Never use INSERT, UPDATE, DELETE, DROP, ALTER,
   CREATE, REPLACE or TRUNCATE.
6. Use only tables and columns present in the schema.
7. For "top N", use ORDER BY and LIMIT.
8. If the user asks for CSE students, determine the
   appropriate column from the schema.
9. If the question asks for students by marks,
   sort marks in descending order.
10. The SQL must be valid SQLite syntax.

Return only the SQL query.
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0,
        max_completion_tokens=1000,
        include_reasoning=False
    )

    sql = response.choices[0].message.content

    return clean_sql(sql)


def run_agent(question: str):

    # Get database structure
    schema = get_schema()

    if schema == "No tables exist in the database.":
        return {
            "success": False,
            "error": "No tables found in the database."
        }

    # Generate SQL using GPT-OSS 20B
    sql = generate_sql(
        question,
        schema
    )

    # Extra safety check
    if not sql.upper().startswith("SELECT"):
        return {
            "success": False,
            "error": "The model generated a non-SELECT query.",
            "sql": sql
        }

    try:

        results = execute_sql(sql)

        return {
            "success": True,
            "question": question,
            "sql": sql,
            "results": results
        }

    except Exception as e:

        return {
            "success": False,
            "question": question,
            "sql": sql,
            "error": str(e)
        }