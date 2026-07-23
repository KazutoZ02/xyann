import os
import io
import asyncio
import discord
from discord import app_commands
from discord.ext import commands
from typing import Dict, List, Optional

import config
from nim_client import NIMClient
from embed_builder import EmbedBuilder
from skills import token_tracker
from web_server import start_web_server, auto_ping_task

# Initialize Discord Bot with intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Clients
nim_client = NIMClient()

# In-memory storage for user states
# user_id -> selected_model_key
user_models: Dict[int, str] = {}

# user_id -> list of message dicts [{"role": "user"/"assistant", "content": "..."}]
user_histories: Dict[int, List[Dict[str, str]]] = {}


class ModelSelectView(discord.ui.View):
    """Interactive Dropdown Menu View for selecting active AI models."""

    def __init__(self, current_model_key: str):
        super().__init__(timeout=120)
        options = []
        for name, data in config.MODEL_REGISTRY.items():
            options.append(
                discord.SelectOption(
                    label=name,
                    value=name,
                    description=data["category"],
                    default=(name == current_model_key)
                )
            )
        
        select = discord.ui.Select(
            placeholder="Choose an AI Model...",
            min_values=1,
            max_values=1,
            options=options
        )
        select.callback = self.select_callback
        self.add_item(select)

    async def select_callback(self, interaction: discord.Interaction):
        selected_key = interaction.data["values"][0]
        user_models[interaction.user.id] = selected_key
        
        embed = discord.Embed(
            title="✅ AI Model Updated",
            description=f"Active model set to **{selected_key}**",
            color=0x76B900
        )
        embed.set_footer(text="All subsequent DMs will use this model.")
        await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.event
async def on_ready():
    print(f"🤖 Bot Online! Logged in as {bot.user.name} (ID: {bot.user.id})")
    
    # Sync Slash Commands globally
    try:
        synced = await bot.tree.sync()
        print(f"⚡ Synced {len(synced)} Slash Command(s)")
    except Exception as e:
        print(f"⚠️ Slash command sync failed: {str(e)}")

    # Start Web Server & Auto-Ping for Render Free Tier Keep-Alive
    asyncio.create_task(start_web_server())
    asyncio.create_task(auto_ping_task())


@bot.event
async def on_message(message: discord.Message):
    # Ignore messages sent by the bot itself
    if message.author == bot.user:
        return

    # Check if message is a Direct Message (DM)
    is_dm = isinstance(message.channel, discord.DMChannel)
    is_mentioned = bot.user in message.mentions
    
    # Process prefix commands first if any
    await bot.process_commands(message)

    # If it's a DM or the bot is mentioned, and not starting with bot prefix '!', treat as AI Chat request
    if (is_dm or is_mentioned) and not message.content.startswith("!"):
        user_id = message.author.id
        
        # Remove the bot mention string from the message content
        user_text = message.content.replace(f'<@{bot.user.id}>', '').replace(f'<@!{bot.user.id}>', '').strip()

        if not user_text:
            return

        # Check if user sent an imagine command in DM
        if user_text.lower().startswith("imagine ") or user_text.lower().startswith("draw "):
            prompt = user_text.split(" ", 1)[1]
            await handle_dm_imagine(message, prompt)
            return

        # Active model key & ID for user
        model_key = user_models.get(user_id, config.DEFAULT_MODEL_KEY)
        model_data = config.MODEL_REGISTRY.get(model_key, config.MODEL_REGISTRY[config.DEFAULT_MODEL_KEY])
        model_id = model_data["id"]
        provider = model_data["provider"]

        # Retrieve conversation history
        history = user_histories.get(user_id, [])
        
        # Build messages payload
        messages_payload = [{"role": "system", "content": config.SYSTEM_PROMPT_GENERAL}]
        
        # Keep up to last 8 turns (16 messages) to optimize tokens
        recent_history = history[-16:]
        messages_payload.extend(recent_history)
        messages_payload.append({"role": "user", "content": user_text})

        # Trigger typing indicator while calling API
        async with message.channel.typing():
            res = await nim_client.chat_completion(
                messages=messages_payload,
                model_id=model_id,
                provider=provider
            )

        if res["error"]:
            embed = EmbedBuilder.build_error_embed("API Error", res["content"])
            await message.channel.send(embed=embed)
            return

        ai_content = res["content"]

        # Append to user context history
        history.append({"role": "user", "content": user_text})
        history.append({"role": "assistant", "content": ai_content})
        user_histories[user_id] = history

        # Format & send Embeds
        embeds = EmbedBuilder.build_chat_embeds(
            user_query=user_text,
            ai_response=ai_content,
            model_name=model_key,
            tokens_info=res
        )

        for embed in embeds:
            await message.channel.send(embed=embed)


async def handle_dm_imagine(message: discord.Message, prompt: str):
    """Helper to process text-to-image request inside DM."""
    async with message.channel.typing():
        # Enhance prompt with skill
        enhanced = await nim_client.enhance_image_prompt(prompt)
        
        model_key = config.DEFAULT_IMAGE_MODEL_KEY
        model_id = config.IMAGE_MODELS[model_key]
        
        res = await nim_client.generate_image(prompt=enhanced, model_id=model_id)

    if res.get("error"):
        embed = EmbedBuilder.build_error_embed("Image Generation Failed", res.get("message", "Unknown Error"))
        await message.channel.send(embed=embed)
        return

    embed = EmbedBuilder.build_image_embed(
        prompt=prompt,
        model_name=model_key,
        latency=res.get("latency", 0.0),
        enhanced_prompt=enhanced
    )

    if "image_bytes" in res:
        file = discord.File(io.BytesIO(res["image_bytes"]), filename="generated_image.png")
        embed.set_image(url="attachment://generated_image.png")
        await message.channel.send(embed=embed, file=file)
    elif "image_url" in res:
        embed.set_image(url=res["image_url"])
        await message.channel.send(embed=embed)


# --- SLASH COMMANDS ---

@bot.tree.command(name="model", description="Switch active AI Model")
async def slash_model(interaction: discord.Interaction):
    current_key = user_models.get(interaction.user.id, config.DEFAULT_MODEL_KEY)
    view = ModelSelectView(current_model_key=current_key)
    
    embed = discord.Embed(
        title="🎛️ Select AI Model",
        description=f"Current Active Model: **{current_key}**\nChoose a new model below:",
        color=0x76B900
    )
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


@bot.tree.command(name="imagine", description="Generate high-quality AI images")
@app_commands.describe(
    prompt="Description of the image you want to generate",
    model="Select image generation model engine",
    enhance="Auto-enhance prompt using Smart Skill"
)
async def slash_imagine(
    interaction: discord.Interaction,
    prompt: str,
    model: Optional[str] = config.DEFAULT_IMAGE_MODEL_KEY,
    enhance: Optional[bool] = True
):
    await interaction.response.defer()

    selected_model_id = config.IMAGE_MODELS.get(model, config.IMAGE_MODELS[config.DEFAULT_IMAGE_MODEL_KEY])

    final_prompt = prompt
    enhanced_prompt_str = None

    if enhance:
        enhanced_prompt_str = await nim_client.enhance_image_prompt(prompt)
        final_prompt = enhanced_prompt_str

    res = await nim_client.generate_image(prompt=final_prompt, model_id=selected_model_id)

    if res.get("error"):
        embed = EmbedBuilder.build_error_embed("Image Generation Failed", res.get("message", "Unknown Error"))
        await interaction.followup.send(embed=embed)
        return

    embed = EmbedBuilder.build_image_embed(
        prompt=prompt,
        model_name=model or config.DEFAULT_IMAGE_MODEL_KEY,
        latency=res.get("latency", 0.0),
        enhanced_prompt=enhanced_prompt_str if enhance else None
    )

    if "image_bytes" in res:
        file = discord.File(io.BytesIO(res["image_bytes"]), filename="generated_image.png")
        embed.set_image(url="attachment://generated_image.png")
        await interaction.followup.send(embed=embed, file=file)
    elif "image_url" in res:
        embed.set_image(url=res["image_url"])
        await interaction.followup.send(embed=embed)


@bot.tree.command(name="tokens", description="View session token consumption and API request metrics")
async def slash_tokens(interaction: discord.Interaction):
    stats = token_tracker.get_summary()
    embed = discord.Embed(
        title="⚡ AI Token & API Usage",
        color=0x76B900
    )
    embed.add_field(name="Prompt Tokens", value=f"`{stats['prompt_tokens']:,}`", inline=True)
    embed.add_field(name="Completion Tokens", value=f"`{stats['completion_tokens']:,}`", inline=True)
    embed.add_field(name="Total Tokens Used", value=f"`{stats['total_tokens']:,}`", inline=True)
    embed.add_field(name="Total API Requests", value=f"`{stats['total_requests']:,}`", inline=True)
    embed.set_footer(text="Xyann • Real-time Metrics")
    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name="clear", description="Clear your current DM conversation history context")
async def slash_clear(interaction: discord.Interaction):
    user_histories.pop(interaction.user.id, None)
    embed = discord.Embed(
        title="🧹 Conversation Context Cleared",
        description="Your DM memory history has been reset for new chat sessions.",
        color=0x76B900
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name="help", description="Show Bot features, available models, and GitHub commands")
async def slash_help(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🚀 Xyann Discord AI Bot",
        description="Welcome to your personal AI Assistant!",
        color=0x76B900
    )
    embed.add_field(
        name="💬 DM Chat",
        value="Send a Direct Message to the bot anytime! Responds in rich Discord Embeds with syntax highlighting & token metrics.",
        inline=False
    )
    embed.add_field(
        name="🎛️ Model Switching (`/model`)",
        value="Switch between various top-tier AI models directly in chat.",
        inline=False
    )
    embed.add_field(
        name="🎨 Image Generation (`/imagine`)",
        value="Generate photorealistic AI images with auto prompt enhancement.",
        inline=False
    )

    embed.add_field(
        name="⚡ Token Tracker (`/tokens`)",
        value="View accumulated prompt and completion token statistics.",
        inline=False
    )
    embed.set_footer(text="Render Free Tier 24/7 Uptime Enabled • Xyann AI")
    await interaction.response.send_message(embed=embed)


if __name__ == "__main__":
    token = config.DISCORD_TOKEN
    if not token or token == "your_discord_bot_token_here":
        print("❌ Error: DISCORD_TOKEN is missing or invalid in environment variables / .env file.")
    else:
        bot.run(token)
