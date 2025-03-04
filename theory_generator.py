from utils import call_llm_api, save_theory_to_cache, get_cached_theory
import random

def generate_unhinged_theory(text: str) -> str:
    """
    Generate a wild, unhinged theory based on user input text.
    
    Args:
        text: The user-provided text containing random information
        
    Returns:
        A generated theory
    """
    # Check if we have a cached theory for similar text
    cached = get_cached_theory(text, mode="unhinged")
    if cached:
        return cached
    
    # Create a simpler prompt for the LLM to generate a theory
    prompt = f"""
    Create a wild, unhinged conspiracy theory based on this input:
    "{text[:300]}"
    
    Make it bizarre but with twisted internal logic.
    Keep it to 2-3 paragraphs.
    """
    
    # Call the LLM API to generate the theory
    theory = call_llm_api(prompt)
    
    # Cache the result
    save_theory_to_cache(text, theory, mode="unhinged")
    
    return theory

def generate_franchise_theory(franchise_name: str, input_text: str = None) -> str:
    """
    Generate a theory based on a named franchise.
    
    Args:
        franchise_name: The name of the franchise (e.g., "Star Wars", "Marvel")
        input_text: Optional additional context or ideas to incorporate
        
    Returns:
        A generated theory about the franchise
    """
    # Create a cache key that includes both franchise name and input text
    cache_key = f"{franchise_name}:{input_text if input_text else ''}"
    
    # Check cache first
    cached = get_cached_theory(cache_key, mode="franchise")
    if cached:
        return cached
    
    # Generate a simpler prompt for the LLM
    prompt = f"""
    Create a wild fan theory about {franchise_name}.
    """
    
    # Add the user's input text if provided
    if input_text and input_text.strip():
        prompt += f" Include these ideas: {input_text[:200]}."
    
    prompt += """
    Make it both surprising and plausible.
    Keep it to 2-3 paragraphs.
    """
    
    # Call the LLM API
    theory = call_llm_api(prompt)
    
    # Cache the result
    save_theory_to_cache(cache_key, theory, mode="franchise")
    
    return theory