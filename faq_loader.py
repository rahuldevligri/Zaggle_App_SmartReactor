import pandas as pd
import openai
import os
import hashlib
import json
import numpy as np
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential
from tqdm import tqdm

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def load_faqs(file_path):
    try:
        df = pd.read_csv(file_path, quotechar='"', escapechar='\\')
        if df.empty:
            raise ValueError("CSV file is empty")
        
        # Clean column names
        df.columns = df.columns.str.strip()\
            .str.lower()\
            .str.replace('[^a-zA-Z0-9]+', '_', regex=True)
        
        required_columns = {'user_query', 'product_responses'}
        if not required_columns.issubset(df.columns):
            missing = required_columns - set(df.columns)
            raise ValueError(f"Missing required columns: {missing}")
            
        # Clean data
        df['user_query'] = df['user_query'].str.strip()
        df['product_responses'] = df['product_responses'].str.strip()
        
        return df
    except Exception as e:
        print(f"❌ Error loading FAQs: {str(e)}")
        raise

def get_cache_key(questions):
    return hashlib.md5(json.dumps(questions).encode()).hexdigest()

def load_cached_embeddings(cache_key):
    try:
        with open(f"embeddings_cache/{cache_key}.npy", "rb") as f:
            return np.load(f).tolist()
    except:
        return None

def save_embeddings_to_cache(cache_key, embeddings):
    os.makedirs("embeddings_cache", exist_ok=True)
    with open(f"embeddings_cache/{cache_key}.npy", "wb") as f:
        np.save(f, np.array(embeddings))

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def embed_batch(batch):
    response = openai.embeddings.create(
        input=batch,
        # model="text-embedding-ada-002"
        model="text-embedding-3-small"
    )
    return [data.embedding for data in response.data]

def embed_faqs(questions):
    cache_key = get_cache_key(questions)
    if cached := load_cached_embeddings(cache_key):
        print("✅ Loaded cached embeddings")
        return cached

    # Clear old cache if exists
    if os.path.exists(f"embeddings_cache/{cache_key}.npy"):
        os.remove(f"embeddings_cache/{cache_key}.npy")
        print("♻️ Cleared incompatible embeddings cache")
    
    batch_size = 100
    embeddings = []
    batches = [questions[i:i + batch_size] 
               for i in range(0, len(questions), batch_size)]
    
    try:
        with tqdm(total=len(questions), desc="📚 Embedding FAQs") as pbar:
            for batch in batches:
                batch_embeddings = embed_batch(batch)
                embeddings.extend(batch_embeddings)
                pbar.update(len(batch))
        save_embeddings_to_cache(cache_key, embeddings)
        return embeddings
    except Exception as e:
        print(f"\n❌ Embedding failed: {str(e)}")
        if "model_not_found" in str(e):
            print("🔥 Critical: Verify OpenAI model access at platform.openai.com/models")
        raise