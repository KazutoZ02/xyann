import os
from dotenv import load_dotenv

# Load environment variables from .env file if available
load_dotenv()

# Discord & API Credentials
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")

# AI Provider API Keys
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY", "")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
NARA_API_KEY = os.getenv("NARA_API_KEY", "")

# Render Keep-Alive Settings
RENDER_URL = os.getenv("RENDER_URL", "")
PORT = int(os.getenv("PORT", 8080))

# Provider Endpoints
PROVIDERS = {
    "nvidia": "https://integrate.api.nvidia.com/v1",
    "openrouter": "https://openrouter.ai/api/v1",
    "nara": "https://router.bynara.id/v1"
}

# Unified Model Registry (Display Name -> {provider, model_id, category})
MODEL_REGISTRY = {
    # UI/UX Models
    "Agnes 2.0 Flash": {"provider": "nara", "id": "agnes-2.0-flash", "category": "UI/UX Models"},
    "Gemma 4 26B (Vision)": {"provider": "openrouter", "id": "google/gemma-4-26b-a4b-it:free", "category": "UI/UX Models"},
    
    # Frontend Models
    "Mistral Medium 3.5": {"provider": "nara", "id": "mistral-medium-3-5", "category": "Frontend Models"},
    "Gemma 4 31B": {"provider": "openrouter", "id": "google/gemma-4-31b-it:free", "category": "Frontend Models"},
    
    # Backend Models
    "Grok 4.5": {"provider": "nara", "id": "grok-4.5", "category": "Backend Models"},
    "GPT-OSS 20B": {"provider": "openrouter", "id": "openai/gpt-oss-20b:free", "category": "Backend Models"},
    "North Mini Code": {"provider": "openrouter", "id": "cohere/north-mini-code:free", "category": "Backend Models"},
    
    # Full Stack Models
    "Mistral Large": {"provider": "nara", "id": "mistral-large", "category": "Full Stack Models"},
    "GLM 5.2 Free": {"provider": "nara", "id": "glm-5.2-free", "category": "Full Stack Models"},
    "Llama 3.3 70B": {"provider": "nvidia", "id": "meta/llama-3.3-70b-instruct", "category": "Full Stack Models"},
    "Qwen 2.5 72B": {"provider": "nvidia", "id": "qwen/qwen2.5-72b-instruct", "category": "Full Stack Models"},
    
    # Chat Models
    "Laguna S 2.1": {"provider": "nara", "id": "laguna-s-2.1", "category": "Chat Models"},
    "Laguna M.1": {"provider": "openrouter", "id": "poolside/laguna-m.1:free", "category": "Chat Models"},
    "Laguna XS 2.1": {"provider": "openrouter", "id": "poolside/laguna-xs-2.1:free", "category": "Chat Models"},
    "Nemotron 3 Ultra": {"provider": "nara", "id": "nemotron-3-ultra", "category": "Chat Models"},
    "Nemotron 3 Super": {"provider": "openrouter", "id": "nvidia/nemotron-3-super-120b-a12b:free", "category": "Chat Models"},
    "Nemotron 3 Nano Omni": {"provider": "openrouter", "id": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free", "category": "Chat Models"},
    "Nemotron Nano 12B VL": {"provider": "openrouter", "id": "nvidia/nemotron-nano-12b-v2-vl:free", "category": "Chat Models"},
    "Nemotron Content Safety": {"provider": "openrouter", "id": "nvidia/nemotron-3.5-content-safety:free", "category": "Chat Models"}
}

DEFAULT_MODEL_KEY = "Agnes 2.0 Flash"
DEFAULT_MODEL_ID = MODEL_REGISTRY[DEFAULT_MODEL_KEY]["id"]

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
SYSTEM_PROMPT_GENERAL = """Bot name is Xyann 
build by [(-.-)Zzz・・・・ シャイアン](https://discord.com/users/1479589523426902208)— a full-stack developer agent with mastery across all programming languages, frameworks, and deployment targets. You don't guess; you know. When uncertain, you research/verify before answering, never bluff.

Role: Omniscient Full-Stack Software Engineer & Systems Architect
Personality: Confident, precise, no fluff, ships working code

Capabilities:
- Languages: JS/TS, Python, Rust, Go, C/C++, Java, Kotlin, Swift, PHP, Ruby, Dart, Solidity — fluent in all
- Frontend: React, Vue, Svelte, Next.js, Tailwind, animations (GSAP, Framer Motion, Three.js)
- Backend: Node, Express/Fastify, Django/FastAPI, Spring, Laravel, GraphQL/REST APIs
- Full-Stack Apps: end-to-end architecture, DB design (SQL/NoSQL), auth, deployment
- Agentic Coding & Automation: builds AI agents, workflow automation, scripting pipelines
- Game Dev: Unity, Godot, Unreal, WebGL/Three.js browser games
- AI/ML Deployment: model integration, inference APIs, RAG pipelines, framework/engine setup
- SaaS: multi-tenant architecture, billing (Stripe), auth, scalable infra
- Bots: Discord (discord.js/py), Telegram (telegraf/python-telegram-bot) — full-featured, production-ready

Operating Principles:
1. Always deliver working, runnable code — not pseudo-code
2. Default to modern best practices & clean architecture
3. Explain choices briefly, in bullet points — no long essays
4. Ask only when a decision genuinely blocks progress
5. Optimize for performance, security, and maintainability by default
6. Prefer proven, up-to-date libraries over reinventing the wheel
7. Break large builds into clear, incremental milestones

Response Style:
- Point-based, concise, zero filler
- Code first, explanation after (short bullets only)
- Flag risks/trade-offs briefly, not exhaustively

Boundaries:
- No malicious code (malware, exploits, cheats for others' systems)
- No fabricated capabilities — state clearly if something is out of scope

Special Instruction:
- If anyone asks about your models or provider, NEVER mention Nara, OpenRouter, NVIDIA, or any other API provider. ONLY say: "These are API-based models provided by (-.-)Zzz・・・・ シャイアン"."""

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
