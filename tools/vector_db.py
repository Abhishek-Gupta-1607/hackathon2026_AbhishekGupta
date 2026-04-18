from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from .common import simulate_failure

# Basic error handling for initialization if model download takes time
try:
    model = SentenceTransformer("all-MiniLM-L6-v2")
except Exception as e:
    print(f"Warning: Model download failed during init. Check connection. {e}")
    # mock fallback if huggingface is down
    model = None

docs = [
    "Refund allowed within 7 days. Returns on electronics take 30 days.",
    "Delivery delays are typically due to local logistics issues. We compensate with a $10 coupon.",
    "Warranty is valid for 1 year from the date of purchase.",
    "For broken items, request an immediate refund and we will cancel the processing queue."
]

if model:
    embeddings = model.encode(docs)
    index = faiss.IndexFlatL2(len(embeddings[0]))
    index.add(np.array(embeddings))
else:
    index = None

def semantic_search(query):
    simulate_failure()
    if not model or not index:
        return "Search degraded: Knowledge Base index unavailable offline."
        
    q_emb = model.encode([query])
    D, I = index.search(np.array(q_emb), k=1)
    
    # Check if the closest match is sufficiently relevant (distance check)
    if D[0][0] > 1.5:
        return "No highly relevant information found in the knowledge base."
        
    return docs[I[0][0]]
