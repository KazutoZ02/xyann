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


class CodeSynthesisSkill:
    """Skill to inspect AI responses, extract code blocks, and format GitHub commit payloads."""
    
    @staticmethod
    def extract_code_blocks(text: str) -> List[Tuple[str, str, str]]:
        """
        Parses text for markdown code blocks.
        Returns a list of tuples: (language, filename_guess, code_content)
        """
        # Pattern to match ```lang filename or ```lang ... ```
        pattern = r"```([a-zA-Z0-9_+\-]*)\s*([^\n]*)\n(.*?)```"
        matches = re.findall(pattern, text, re.DOTALL)
        
        extracted = []
        for idx, (lang, header_info, content) in enumerate(matches):
            lang = lang.strip().lower() or "text"
            header_info = header_info.strip()
            
            # Check if header contains a valid filename (e.g. main.py, index.js)
            filename = ""
            if header_info and ("." in header_info or "/" in header_info):
                filename = header_info.split()[0]
            else:
                ext_map = {
                    "python": "py", "javascript": "js", "typescript": "ts",
                    "html": "html", "css": "css", "json": "json", "markdown": "md",
                    "cpp": "cpp", "c": "c", "java": "java", "go": "go", "rust": "rs", "sh": "sh"
                }
                ext = ext_map.get(lang, "txt")
                filename = f"snippet_{idx+1}.{ext}"
                
            extracted.append((lang, filename, content.strip()))
            
        return extracted


class ImagePromptSkill:
    """Skill to optimize short user prompts into rich visual descriptions for FLUX/SD3.5."""
    
    @staticmethod
    def format_enhanced_prompt(user_prompt: str) -> str:
        """Fallback lightweight local prompt enhancement if LLM expansion is bypassed."""
        quality_keywords = "photorealistic, 8k resolution, highly detailed, cinematic lighting, masterpiece"
        if not any(k in user_prompt.lower() for k in ["photorealistic", "8k", "cinematic", "detailed"]):
            return f"{user_prompt}, {quality_keywords}"
        return user_prompt
