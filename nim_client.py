import time
import base64
import aiohttp
from typing import Dict, Any, Tuple, Optional, List
import config
from skills import token_tracker, ImagePromptSkill

class NIMClient:
    """Async Client for NVIDIA NIM REST API endpoints (OpenAI compatible)."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or config.NVIDIA_API_KEY
        self.base_url = config.NVIDIA_NIM_BASE_URL.rstrip('/')

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model_id: str = config.DEFAULT_MODEL_ID,
        temperature: float = config.TEMPERATURE,
        max_tokens: int = config.MAX_TOKENS,
        top_p: float = config.TOP_P
    ) -> Dict[str, Any]:
        """
        Sends a chat completion request to NVIDIA NIM API.
        Returns dict with: content, prompt_tokens, completion_tokens, latency, error
        """
        if not self.api_key:
            return {
                "content": "❌ Error: `NVIDIA_API_KEY` is not set in environment variables.",
                "prompt_tokens": 0, "completion_tokens": 0, "latency": 0.0, "error": True
            }

        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": model_id,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p
        }

        start_time = time.time()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=self._get_headers(), json=payload, timeout=90) as response:
                    latency = round(time.time() - start_time, 2)
                    if response.status != 200:
                        err_text = await response.text()
                        return {
                            "content": f"⚠️ NVIDIA NIM API Error ({response.status}):\n```{err_text[:800]}```",
                            "prompt_tokens": 0, "completion_tokens": 0, "latency": latency, "error": True
                        }

                    data = await response.json()
                    
                    choice = data.get("choices", [{}])[0]
                    message_data = choice.get("message", {})
                    content = message_data.get("content", "").strip()

                    # Handle DeepSeek R1 reasoning/think tags if present
                    if not content and "reasoning_content" in message_data:
                        content = message_data["reasoning_content"]

                    usage = data.get("usage", {})
                    p_tokens = usage.get("prompt_tokens", 0)
                    c_tokens = usage.get("completion_tokens", 0)

                    # Update global token skill tracker
                    token_tracker.record_usage(p_tokens, c_tokens)

                    return {
                        "content": content or "*(Empty response received from model)*",
                        "prompt_tokens": p_tokens,
                        "completion_tokens": c_tokens,
                        "latency": latency,
                        "error": False
                    }
        except Exception as e:
            latency = round(time.time() - start_time, 2)
            return {
                "content": f"❌ Exception during NVIDIA NIM API call:\n```{repr(e)}```",
                "prompt_tokens": 0, "completion_tokens": 0, "latency": latency, "error": True
            }

    async def generate_image(
        self,
        prompt: str,
        model_id: str = config.IMAGE_MODELS[config.DEFAULT_IMAGE_MODEL_KEY]
    ) -> Dict[str, Any]:
        """
        Generates an image via NVIDIA NIM /v1/images/generations endpoint.
        Returns dict with: image_url or image_bytes (base64 decoded), prompt, latency, error
        """
        if not self.api_key:
            return {"error": True, "message": "NVIDIA_API_KEY missing."}

        url = f"{self.base_url}/images/generations"
        payload = {
            "model": model_id,
            "prompt": prompt,
            "n": 1,
            "size": "1024x1024",
            "response_format": "b64_json"
        }

        start_time = time.time()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=self._get_headers(), json=payload, timeout=120) as response:
                    latency = round(time.time() - start_time, 2)
                    if response.status != 200:
                        err_text = await response.text()
                        return {
                            "error": True,
                            "message": f"NVIDIA Image API Error ({response.status}):\n```{err_text[:500]}```",
                            "latency": latency
                        }

                    data = await response.json()
                    image_items = data.get("data", [])
                    if not image_items:
                        return {"error": True, "message": "No image data returned from NIM.", "latency": latency}

                    item = image_items[0]
                    if "b64_json" in item:
                        img_bytes = base64.b64decode(item["b64_json"])
                        return {"error": False, "image_bytes": img_bytes, "latency": latency}
                    elif "url" in item:
                        return {"error": False, "image_url": item["url"], "latency": latency}
                    else:
                        return {"error": True, "message": "Unrecognized image payload format.", "latency": latency}
        except Exception as e:
            latency = round(time.time() - start_time, 2)
            return {"error": True, "message": f"Image generation failed: {str(e)}", "latency": latency}

    async def enhance_image_prompt(self, user_prompt: str) -> str:
        """Uses fast NIM LLM to refine short user prompts into descriptive image prompts."""
        messages = [
            {"role": "system", "content": config.SYSTEM_PROMPT_IMAGE_ENHANCER},
            {"role": "user", "content": f"Enhance this image prompt for FLUX.1: '{user_prompt}'"}
        ]
        res = await self.chat_completion(messages, model_id=config.TEXT_MODELS["DeepSeek V4 Flash"], max_tokens=150)
        if not res["error"] and res["content"]:
            return res["content"].strip('"').strip("'")
        return ImagePromptSkill.format_enhanced_prompt(user_prompt)
