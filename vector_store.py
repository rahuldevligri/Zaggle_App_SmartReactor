import faiss
import numpy as np

class FAQVectorStore:
    def __init__(self, embeddings, faq_df):
        self.faq_df = faq_df
        self.dimension = len(embeddings[0]) if embeddings else 0
        self.index = faiss.IndexFlatL2(self.dimension)

        if embeddings:
            self.index.add(np.array(embeddings).astype('float32'))

    def search(self, query_embedding, top_k=1):
        if self.dimension == 0 or self.index.ntotal == 0:
            raise ValueError("Vector store contains no embeddings")
            
        query_array = np.array([query_embedding]).astype('float32')
        if query_array.shape[1] != self.dimension:
            raise ValueError(f"Query dimension mismatch: {query_array.shape[1]} vs {self.dimension}")
        
        distances, indices = self.index.search(query_array, top_k)
        return self.faq_df.iloc[indices[0][0]]