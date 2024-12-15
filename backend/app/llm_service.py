import os
import json
import hashlib
import time
from typing import List
from dotenv import load_dotenv
from groq import Groq
import shutil

load_dotenv()

class LLMService:
    def __init__(self, max_cache_entries: int = 2):
        """
        Initialize LLM Service with LRU persistent caching
        
        Args:
            max_cache_entries (int): Maximum number of cached entries
        """
        self.client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        self.cache_dir = "data/llm_cache"
        self.max_cache_entries = max_cache_entries
        
        # Ensure cache directory exists
        os.makedirs(self.cache_dir, exist_ok=True)

    def _generate_cache_key(self, query: str, context: List[str]) -> str:
        """
        Generate a unique cache key for a query and context
        """
        cache_input = json.dumps({
            'query': query.lower(), 
            'context': context
        }, sort_keys=True)
        
        return hashlib.md5(cache_input.encode()).hexdigest()

    def _get_cache_entries(self):
        """
        Get all cache entries sorted by timestamp (least recently used first)
        
        Returns:
            List[dict]: Sorted list of cache entries
        """
        entries = []
        for filename in os.listdir(self.cache_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.cache_dir, filename)
                try:
                    with open(filepath, 'r') as f:
                        entry = json.load(f)
                        entry['filepath'] = filepath
                        entry['filename'] = filename
                        entries.append(entry)
                except (json.JSONDecodeError, FileNotFoundError):
                    # Remove invalid cache files
                    os.remove(filepath)
        
        # Sort entries by timestamp (least recently used first)
        return sorted(entries, key=lambda x: x.get('timestamp', 0))

    def generate_response(self, query: str, context: List[str]) -> str:
        """
        Generate response with LRU persistent caching
        """
        # Generate cache key
        cache_key = self._generate_cache_key(query, context)
        cache_path = os.path.join(self.cache_dir, f"{cache_key}.json")
        
        # Check if already cached
        if os.path.exists(cache_path):
            with open(cache_path, 'r') as f:
                cached_entry = json.load(f)
            
            # Update timestamp to make it most recently used
            cached_entry['timestamp'] = time.time()
            
            # Write back the updated entry
            with open(cache_path, 'w') as f:
                json.dump(cached_entry, f)
            
            return cached_entry['response']
        
        # Manage cache size before adding new entry
        entries = self._get_cache_entries()
        while len(entries) >= self.max_cache_entries:
            # Remove oldest entry (least recently used)
            oldest_entry = entries.pop(0)
            try:
                os.remove(oldest_entry['filepath'])
            except FileNotFoundError:
                pass
        
        # Generate response
        context_text = "\n\n".join(context)
        prompt = f"""Please answer the question based only on the following context. If the answer cannot be found in the context, say so.

Context:
{context_text}

Question: {query}

Answer:"""

        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that answers questions based solely on the provided context."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="gemma2-9b-it",
            temperature=0.1,
        )
        
        response = chat_completion.choices[0].message.content
        
        # Save to cache with current timestamp
        cache_entry = {
            'response': response,
            'timestamp': time.time(),
            'query': query,
            'context': context
        }
        
        with open(cache_path, 'w') as f:
            json.dump(cache_entry, f)
        
        return response

    def clear_cache(self):
        """
        Clear all cached entries
        """
        try:
            shutil.rmtree(self.cache_dir)
            os.makedirs(self.cache_dir, exist_ok=True)
        except Exception as e:
            print(f"Error clearing cache: {e}")

    def get_cache_info(self):
        """
        Get information about the current cache
        """
        cache_files = [f for f in os.listdir(self.cache_dir) if f.endswith('.json')]
        return {
            "total_entries": len(cache_files),
            "max_entries": self.max_cache_entries
        }
    

# import os
# from dotenv import load_dotenv
# from groq import Groq
# from typing import List

# load_dotenv()


# class LLMService:
#     def __init__(self):
#         self.client = Groq(api_key=os.getenv('GROQ_API_KEY'))

#     def generate_response(self, query: str, context: List[str]) -> str:
#         """Generate response using Groq API"""
#         context_text = "\n\n".join(context)
#         prompt = f"""Please answer the question based only on the following context. If the answer cannot be found in the context, say so.

# Context:
# {context_text}

# Question: {query}

# Answer:"""

#         chat_completion = self.client.chat.completions.create(
#             messages=[
#                 {
#                     "role": "system",
#                     "content": "You are a helpful assistant that answers questions based solely on the provided context."
#                 },
#                 {
#                     "role": "user",
#                     "content": prompt
#                 }
#             ],
#             model="gemma2-9b-it",
#             temperature=0.1,
#         )
        
#         return chat_completion.choices[0].message.content

