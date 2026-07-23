import re
import time
from typing import Dict, Any, List, Tuple

class TokenTracker:
    """Skill to measure and track real-time API token usage and latency."""
    def __init__(self):
        self.session_prompt_tokens = 0
        self.session_completion_tokens = 0
        self.session_requests = 0

    def record_usage(self, prompt_tokens: int, completion_tokens: int):
        self.session_prompt_tokens += prompt_tokens
        self.session_completion_tokens += completion_tokens
        self.session_requests += 1

    def get_summary(self) -> Dict[str, Any]:
        total = self.session_prompt_tokens + self.session_completion_tokens
        return {
            "prompt_tokens": self.session_prompt_tokens,
            "completion_tokens": self.session_completion_tokens,
            "total_tokens": total,
            "total_requests": self.session_requests
        }

# Global singleton token tracker
token_tracker = TokenTracker()





class ImagePromptSkill:
    """Skill to optimize short user prompts into rich visual descriptions for FLUX/SD3.5."""
    
    @staticmethod
    def format_enhanced_prompt(user_prompt: str) -> str:
        """Fallback lightweight local prompt enhancement if LLM expansion is bypassed."""
        quality_keywords = "photorealistic, 8k resolution, highly detailed, cinematic lighting, masterpiece"
        if not any(k in user_prompt.lower() for k in ["photorealistic", "8k", "cinematic", "detailed"]):
            return f"{user_prompt}, {quality_keywords}"
        return user_prompt
