"""
Vector Database Module
Handles FAISS vector database creation, embeddings, and similarity search
"""

import os
import pickle
import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Tuple


class VectorDatabase:
    """Manages vector embeddings and FAISS-based similarity search"""
    
    def __init__(self, csv_path: str = "maharashtra_schemes.csv", 
                 cache_dir: str = "cache",
                 model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the Vector Database
        
        Args:
            csv_path: Path to the CSV file containing schemes
            cache_dir: Directory to store cached FAISS index
            model_name: Sentence transformer model name
        """
        self.csv_path = csv_path
        self.cache_dir = cache_dir
        self.model_name = model_name
        self.embedder = None
        self.index = None
        self.schemes_data = None
        self.index_path = os.path.join(cache_dir, "faiss_index.pkl")
        
        # Create cache directory if it doesn't exist
        os.makedirs(cache_dir, exist_ok=True)
    
    def _load_model(self):
        """Load the sentence transformer model"""
        if self.embedder is None:
            print(f"Loading embedding model: {self.model_name}")
            self.embedder = SentenceTransformer(self.model_name)
    
    def _load_data(self):
        """Load and preprocess the CSV data"""
        if self.schemes_data is None:
            print(f"Loading data from {self.csv_path}")
            df = pd.read_csv(self.csv_path)
            self.schemes_data = df.to_dict('records')
            print(f"Loaded {len(self.schemes_data)} schemes")
    
    def _combine_scheme_fields(self, scheme: Dict) -> str:
        """
        Combine all scheme fields into a single text for embedding
        
        Args:
            scheme: Dictionary containing scheme data
            
        Returns:
            Combined text string
        """
        fields = [
            f"Scheme Name: {scheme.get('Scheme Name', '')}",
            f"Details: {scheme.get('Details', '')}",
            f"Benefits: {scheme.get('Benefits', '')}",
            f"Eligibility: {scheme.get('Eligibility', '')}",
            f"Application Process: {scheme.get('Application Process', '')}",
            f"Documents Required: {scheme.get('Documents Required', '')}"
        ]
        return " ".join(fields)
    
    def _create_embeddings(self) -> np.ndarray:
        """
        Create embeddings for all schemes
        
        Returns:
            Numpy array of embeddings
        """
        print("Creating embeddings for schemes...")
        combined_texts = [self._combine_scheme_fields(scheme) 
                          for scheme in self.schemes_data]
        embeddings = self.embedder.encode(combined_texts, show_progress_bar=True)
        print(f"Created embeddings of shape: {embeddings.shape}")
        return embeddings
    
    def _create_faiss_index(self, embeddings: np.ndarray) -> faiss.Index:
        """
        Create and populate FAISS index
        
        Args:
            embeddings: Numpy array of embeddings
            
        Returns:
            FAISS index object
        """
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)
        
        index.add(embeddings.astype('float32'))
        print(f"FAISS index created with {index.ntotal} vectors")
        return index
    
    def _save_index(self, index: faiss.Index):
        """Save FAISS index and schemes data to disk"""
        print(f"Saving index to {self.index_path}")
        with open(self.index_path, 'wb') as f:
            pickle.dump({
                'index': index,
                'schemes_data': self.schemes_data
            }, f)
        print("Index saved successfully")
    
    def _load_index(self) -> bool:
        """
        Load FAISS index from disk
        
        Returns:
            True if loaded successfully, False otherwise
        """
        if not os.path.exists(self.index_path):
            print("No cached index found")
            return False
        
        try:
            print(f"Loading index from {self.index_path}")
            with open(self.index_path, 'rb') as f:
                data = pickle.load(f)
                self.index = data['index']
                self.schemes_data = data['schemes_data']
            print("Index loaded successfully")
            return True
        except Exception as e:
            print(f"Error loading index: {e}")
            return False
    
    def initialize(self):
        """
        Initialize the vector database
        Tries to load from cache first, otherwise creates new index
        """
        # Load data first
        self._load_data()
        
        # Try to load cached index
        if self._load_index():
            return
        
        # Create new index if cache doesn't exist
        print("Creating new FAISS index...")
        self._load_model()
        embeddings = self._create_embeddings()
        self.index = self._create_faiss_index(embeddings)
        self._save_index(self.index)
    
    def search_schemes(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Search for most relevant schemes based on query
        
        Args:
            query: User query string
            top_k: Number of top results to return
            
        Returns:
            List of relevant scheme dictionaries
        """
        if self.index is None or self.schemes_data is None:
            raise ValueError("Database not initialized. Call initialize() first.")
        
        if self.embedder is None:
            self._load_model()
        
        # Create query embedding
        query_embedding = self.embedder.encode([query])
        query_embedding = np.array(query_embedding, dtype='float32')
        faiss.normalize_L2(query_embedding)
        
        # Search in FAISS index - increase search to allow for reranking
        search_k = min(top_k * 3, len(self.schemes_data))
        distances, indices = self.index.search(query_embedding, search_k)
        
        # Retrieve schemes with scores
        candidate_schemes = []
        query_lower = query.lower()
        
        for idx, score in zip(indices[0], distances[0]):
            if idx >= len(self.schemes_data):
                continue
            scheme = self.schemes_data[idx].copy()
            scheme_name_lower = scheme.get('Scheme Name', '').lower()
            
            # Boost score if scheme name matches query keywords
            boosted_score = float(score)
            if any(word in scheme_name_lower for word in query_lower.split() if len(word) > 3):
                # Boost similarity if scheme name contains query keywords
                boosted_score = min(boosted_score * 1.2, 1.0)
            
            # Extra boost for exact scheme name matches
            scheme_keywords = ['indira gandhi', 'widow pension', 'old age pension', 'disability pension', 
                              'mahila samridhi', 'samridhi yojana', 'mahila kisan', 'ramai awas', 'gharkul']
            if any(keyword in scheme_name_lower and keyword in query_lower for keyword in scheme_keywords):
                boosted_score = min(boosted_score * 1.3, 1.0)
            
            # Special boost: remove "(Maharashtra)" and other location suffixes for matching
            scheme_name_clean = scheme_name_lower.replace('(maharashtra)', '').replace('(urban)', '').replace('(rural)', '').strip()
            query_clean = query_lower.replace('(maharashtra)', '').replace('(urban)', '').replace('(rural)', '').strip()
            
            # If core scheme name words match (after removing suffixes), boost more
            scheme_words = set([w for w in scheme_name_clean.split() if len(w) > 3])
            query_words = set([w for w in query_clean.split() if len(w) > 3])
            matching_words = scheme_words.intersection(query_words)
            
            if len(matching_words) >= 2:  # At least 2 significant words match
                boosted_score = min(boosted_score * 1.25, 1.0)
            
            scheme['similarity_score'] = boosted_score
            candidate_schemes.append((boosted_score, scheme))
        
        # Sort by boosted score
        candidate_schemes.sort(key=lambda x: x[0], reverse=True)
        
        # Filter by minimum similarity threshold (cosine similarity of 0.3 or higher)
        # This helps ensure only reasonably relevant schemes are returned
        min_similarity = 0.25  # Adjusted threshold for better recall
        filtered_schemes = [(score, scheme) for score, scheme in candidate_schemes if score >= min_similarity]
        
        # Return top_k schemes above threshold, or at least the top result even if below threshold
        # This ensures we don't return empty results for edge cases
        if filtered_schemes:
            results = [scheme for _, scheme in filtered_schemes[:top_k]]
        elif candidate_schemes:
            # Fallback: return at least top 1 even if below threshold (for edge cases)
            results = [scheme for _, scheme in candidate_schemes[:1]]
        else:
            results = []
        
        return results


def get_vector_db() -> VectorDatabase:
    """
    Factory function to create and initialize vector database
    Uses caching to avoid reinitializing
    
    Returns:
        Initialized VectorDatabase instance
    """
    db = VectorDatabase()
    db.initialize()
    return db

