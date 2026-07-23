import asyncio
import os
import sys

# Ensure stdout handles UTF-8 output on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import config
from skills import token_tracker, CodeSynthesisSkill, ImagePromptSkill
from embed_builder import EmbedBuilder
from nim_client import NIMClient
from github_client import GitHubClient
from web_server import start_web_server
import aiohttp

async def run_tests():
    print("=" * 60)
    print("RUNNING BOT MODULE TEST SUITE")
    print("=" * 60)

    # 1. Config Test
    print("\n1. Testing config.py...")
    assert len(config.TEXT_MODELS) >= 9, "TEXT_MODELS catalog incomplete"
    assert config.DEFAULT_MODEL_KEY in config.TEXT_MODELS, "Default model key missing"
    assert len(config.IMAGE_MODELS) >= 2, "IMAGE_MODELS catalog incomplete"
    print(f"   [SUCCESS] Config verified! Total Models: {len(config.TEXT_MODELS)} Text LLMs, {len(config.IMAGE_MODELS)} Image Models.")

    # 2. Skills Test
    print("\n2. Testing skills.py...")
    token_tracker.record_usage(150, 350)
    summary = token_tracker.get_summary()
    assert summary["prompt_tokens"] == 150
    assert summary["completion_tokens"] == 350
    assert summary["total_tokens"] == 500
    print(f"   [SUCCESS] TokenTracker Skill verified! Summary: {summary}")

    sample_md = (
        "Here is the Python code:\n"
        "```python main.py\nprint('Hello World')\n```\n"
        "And here is HTML:\n"
        "```html index.html\n<h1>Title</h1>\n```"
    )
    blocks = CodeSynthesisSkill.extract_code_blocks(sample_md)
    assert len(blocks) == 2
    assert blocks[0][1] == "main.py"
    assert blocks[1][1] == "index.html"
    print(f"   [SUCCESS] CodeSynthesisSkill verified! Extracted {len(blocks)} code block files: {[b[1] for b in blocks]}")

    enhanced = ImagePromptSkill.format_enhanced_prompt("a cute robot cat")
    assert "photorealistic" in enhanced
    print(f"   [SUCCESS] ImagePromptSkill verified! Enhanced prompt: '{enhanced}'")

    # 3. Embed Builder Test
    print("\n3. Testing embed_builder.py...")
    long_response = "Line of AI response text.\n" * 200
    embeds = EmbedBuilder.build_chat_embeds(
        user_query="Write code",
        ai_response=long_response,
        model_name="DeepSeek V4 Pro",
        tokens_info={"prompt_tokens": 100, "completion_tokens": 500, "latency": 1.25}
    )
    assert len(embeds) >= 1
    print(f"   [SUCCESS] EmbedBuilder verified! Generated {len(embeds)} chunked Discord Embed(s).")

    # 4. Graceful Error Handling Test (Without API Tokens)
    print("\n4. Testing NIM & GitHub Client Graceful Handling without tokens...")
    nim = NIMClient(api_key="")
    chat_res = await nim.chat_completion(messages=[{"role": "user", "content": "hi"}])
    assert chat_res["error"] is True
    print("   [SUCCESS] NIMClient handled missing key gracefully (No crashes).")

    gh = GitHubClient(token="")
    gh_res = await gh.create_repository("test-repo")
    assert gh_res["success"] is False
    print("   [SUCCESS] GitHubClient handled missing token gracefully (No crashes).")

    # 5. Web Server Test
    print("\n5. Testing web_server.py HTTP Server...")
    await start_web_server()
    await asyncio.sleep(0.5)

    async with aiohttp.ClientSession() as session:
        async with session.get("http://127.0.0.1:8080/") as resp:
            assert resp.status == 200
            json_data = await resp.json()
            assert json_data["status"] == "online"
            print(f"   [SUCCESS] Embedded Web Server Health Endpoint Verified! Response: {json_data}")

    print("\n" + "=" * 60)
    print("ALL MODULE TESTS PASSED WITH 100% SUCCESS!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(run_tests())
