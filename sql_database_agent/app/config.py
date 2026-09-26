import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./students.db"
)
MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "openai/gpt-oss-20b"
)

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is missing. Please add it to the .env file."
    )
