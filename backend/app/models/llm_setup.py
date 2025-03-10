import google.generativeai as genai
# from langchain_community.llms import GoogleGenerativeAI
from langchain_google_genai import ChatGoogleGenerativeAI
from ..config import GEMINI_API_KEY, MODEL_NAME, DEFAULT_TEMPERATURE

def initialize_gemini():
    """Initialize the Gemini API client."""
    genai.configure(api_key=GEMINI_API_KEY)
    return genai

def create_gemini_llm(temperature=DEFAULT_TEMPERATURE):
    """Create and configure the Gemini LLM for LangChain."""
    # Initialize Gemini API
    initialize_gemini()
    
    # Return the LangChain compatible model
    return ChatGoogleGenerativeAI(
        api_key=GEMINI_API_KEY,
        model=MODEL_NAME,
        temperature=temperature,
        convert_system_message_to_human=True  # Gemini handles system prompts differently
    )

def create_gemini_raw_client():
    """Create a direct Gemini client for advanced configuration."""
    # Initialize Gemini API
    gemini = initialize_gemini()
    
    # Configure the model
    generation_config = {
        "temperature": DEFAULT_TEMPERATURE,
        "top_p": 0.9,
        "top_k": 40,
        "max_output_tokens": 2048,
    }
    
    # Create the model
    model = gemini.GenerativeModel(
        model_name=MODEL_NAME,
        generation_config=generation_config
    )
    
    return model