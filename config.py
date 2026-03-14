import os
from dotenv import load_dotenv

load_dotenv()

# LeetCode GraphQL API endpoint
LEETCODE_API_URL = "https://leetcode.com/graphql"

# Email Configuration
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # Use App Password for Gmail
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# LLM Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "google/gemini-2.0-flash-001")

# Storage Configuration
DB_PATH = os.path.join(os.path.dirname(__file__), "leetcode_history.db")

# Default Problem Constraints
PROBLEM_COUNT = 5
DEFAULT_DIFFICULTIES = ["Easy", "Medium"]
DEFAULT_TAGS = []
