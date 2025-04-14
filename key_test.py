import openai
import os
from dotenv import load_dotenv
load_dotenv()

key = os.getenv("OPENAI_API_KEY")
print("API key exists?", bool(key))
print(f"Key: {key[:5]}...{key[-4:]}")

try:
    openai.embeddings.create(
        input="test",
        # model="text-embedding-ada-002"
        model="text-embedding-3-small"
    )
    print("✅ Valid key!")
except Exception as e:
    print("❌ Error:", str(e))