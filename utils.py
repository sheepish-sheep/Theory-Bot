import json
import os
import requests
from typing import Dict, Optional, Any
import hashlib
import re

# Configuration
LLM_API_URL = "http://127.0.0.1:1234/v1/completions"
CACHE_FILE = "cached_theories.json"

def call_llm_api(prompt: str) -> str:
    """
    Call the local LLM API (LM Studio) to generate text based on a prompt.
    
    Args:
        prompt: The prompt to send to the LLM
        
    Returns:
        The generated text response
    """
    try:
        print(f"Sending request to LLM API at {LLM_API_URL}...")
        response = requests.post(
            LLM_API_URL,
            json={
                "model": "hermes-2-llama-3.1-8b", 
                "prompt": prompt,
                "max_tokens": 800,
                "temperature": 0.7,
                "top_p": 0.9,
                "stop": None
            },
            timeout=60  # Increased timeout to 60 seconds
        )

        # Raise an exception if the request failed
        response.raise_for_status()
        
        # Parse the response
        result = response.json()
        print("Received response from LLM API")
        
        # Extract the generated text
        text = result["choices"][0]["text"]
        
        # Clean the text of special tokens
        cleaned_text = clean_special_tokens(text)
        
        return cleaned_text
    
    except requests.exceptions.Timeout:
        error_msg = "The request to the LLM API timed out. The model might need more time to generate a response. Try again or use a smaller prompt."
        print(f"Error: {error_msg}")
        return f"Error: {error_msg}"
    except requests.exceptions.ConnectionError:
        error_msg = "Could not connect to the LLM API. Make sure LM Studio is running and accessible."
        print(f"Error: {error_msg}")
        return f"Error: {error_msg}"
    except Exception as e:
        print(f"Error calling LLM API: {str(e)}")
        return f"Error generating theory: {str(e)}"

def clean_special_tokens(text: str) -> str:
    """
    Clean special tokens and unwanted content from the LLM output.
    
    Args:
        text: The text to clean
        
    Returns:
        Cleaned text
    """
    # Clean LLM special tokens
    patterns = [
        r'<\|end_of_text\|>',
        r'<\|begin_of_text\|>',
        r'://>', 
        r'_REF\d+',
        r'{if!nbsp;.*?}',  # Match the {if!nbsp;...} pattern
        r'nbsp;',
        r'\.Formspringendon',  # Remove Formspring references
    ]
    
    cleaned = text
    for pattern in patterns:
        cleaned = re.sub(pattern, '', cleaned)
    
    # Remove HTML tags
    cleaned = re.sub(r'<[^>]*>', '', cleaned)
    
    # Remove code blocks (content between ``` marks)
    cleaned = re.sub(r'```[\s\S]*?```', '', cleaned)
    
    # Remove URLs
    cleaned = re.sub(r'https?://\S+', '', cleaned)
    
    # Remove repeated whitespace
    cleaned = re.sub(r'\s+', ' ', cleaned)
    
    # Fix spacing after punctuation
    cleaned = re.sub(r'(\w)\.(\w)', r'\1. \2', cleaned)
    cleaned = re.sub(r'(\w),(\w)', r'\1, \2', cleaned)
    
    return cleaned.strip()

def _get_cache() -> Dict:
    """
    Load the cache from the file or create a new one if it doesn't exist.
    
    Returns:
        The cache dictionary
    """
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Error: {CACHE_FILE} is corrupted. Creating new cache.")
            return {"unhinged": {}, "franchise": {}}
    else:
        return {"unhinged": {}, "franchise": {}}

def _save_cache(cache: Dict) -> None:
    """
    Save the cache to the file.
    
    Args:
        cache: The cache dictionary to save
    """
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


def _compute_input_hash(input_text: str) -> str:
    """
    Compute a hash of the input text to use as a cache key.
    
    Args:
        input_text: The input text to hash
        
    Returns:
        A hash string
    """
    return hashlib.md5(input_text.lower().encode()).hexdigest()

def get_cached_theory(input_text: str, mode: str) -> Optional[str]:
    """
    Get a theory from the cache if it exists.
    
    Args:
        input_text: The input text or franchise name
        mode: Either "unhinged" or "franchise"
        
    Returns:
        The cached theory or None if not found
    """
    cache = _get_cache()
    input_hash = _compute_input_hash(input_text)
    if mode in cache and input_hash in cache[mode]:
        return cache[mode][input_hash]
    return None

def save_theory_to_cache(input_text: str, theory: str, mode: str) -> None:
    """
    Save a generated theory to the cache.
    
    Args:
        input_text: The input text or franchise name
        theory: The generated theory
        mode: Either "unhinged" or "franchise"
    """
    cache = _get_cache()
    input_hash = _compute_input_hash(input_text)

    if mode not in cache:
        cache[mode] = {}

    cache[mode][input_hash] = theory
    _save_cache(cache)
