import os
from dotenv import load_dotenv

# Load environment variables from .env file if available
load_dotenv()

# Discord & API Credentials
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "")
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY", "")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")

# Render Keep-Alive Settings
RENDER_URL = os.getenv("RENDER_URL", "")
PORT = int(os.getenv("PORT", 8080))

# NVIDIA NIM API Base Endpoint
NVIDIA_NIM_BASE_URL = "https://integrate.api.nvidia.com/v1"

# Curated & Configured Text/Code LLM Models
TEXT_MODELS = {
    "Llama 3.3 70B": "meta/llama-3.3-70b-instruct",
    "Nemotron 70B": "nvidia/llama-3.1-nemotron-70b-instruct"
}

DEFAULT_MODEL_KEY = "Llama 3.3 70B"
DEFAULT_MODEL_ID = TEXT_MODELS[DEFAULT_MODEL_KEY]

# NVIDIA NIM Image Generation Models
IMAGE_MODELS = {
    "FLUX.1 Schnell": "black-forest-labs/flux-1-schnell",
    "Stable Diffusion 3.5 Large": "stabilityai/stable-diffusion-3.5-large"
}

DEFAULT_IMAGE_MODEL_KEY = "FLUX.1 Schnell"

# Max Effort Inference Parameters
MAX_TOKENS = 4096
TEMPERATURE = 0.7
TOP_P = 0.95

# System Prompts
SYSTEM_PROMPT_GENERAL = (
    "You are Antigravity Discord AI, an elite AI assistant powered by NVIDIA NIM endpoints. "
    "Provide extremely thorough, precise, high-effort answers. Format your output using clean markdown. "
    "When asked to write code, provide full, runnable production code with complete syntax highlighting."
)

SYSTEM_PROMPT_CODE = (
    "You are an expert senior software engineer and architect powered by NVIDIA NIM. "
    "Write production-grade, bug-free, fully commented code. Always wrap complete code blocks in markdown "
    "with clear file names or language tags (e.g. ```python main.py ... ```)."
)

SYSTEM_PROMPT_IMAGE_ENHANCER = (
    "You are an expert generative AI prompt engineer for FLUX.1 and Stable Diffusion 3.5. "
    "Transform short user image requests into rich, detailed, vivid, photorealistic image prompts. "
    "Return ONLY the final enhanced prompt text without conversational preamble or quotes."
)
