import discord
from typing import List, Dict, Any, Optional
import datetime

# Custom Palette Colors
COLOR_NVIDIA_GREEN = 0x76B900
COLOR_DARK_PURPLE = 0x5865F2
COLOR_ERROR_RED = 0xED4245
COLOR_GITHUB_BLACK = 0x24292E

class EmbedBuilder:
    """Helper to format Discord Embeds with token metrics, syntax highlighting, and chunking."""

    @staticmethod
    def build_chat_embeds(
        user_query: str,
        ai_response: str,
        model_name: str,
        tokens_info: Dict[str, Any],
        author_name: str = "NVIDIA NIM AI",
        author_icon: Optional[str] = None
    ) -> List[discord.Embed]:
        """
        Splits a long AI chat response into multiple Discord Embeds compliant with limits (4096 chars per embed).
        """
        # Chunk response into max 3900 character slices to ensure embed bounds
        max_chunk_size = 3800
        chunks = []
        
        remaining = ai_response
        while remaining:
            if len(remaining) <= max_chunk_size:
                chunks.append(remaining)
                break
            
            # Find last newline near cutoff point
            split_idx = remaining.rfind("\n", 0, max_chunk_size)
            if split_idx == -1 or split_idx < 1000:
                split_idx = max_chunk_size
                
            chunks.append(remaining[:split_idx])
            remaining = remaining[split_idx:].lstrip("\n")

        embeds = []
        p_tok = tokens_info.get("prompt_tokens", 0)
        c_tok = tokens_info.get("completion_tokens", 0)
        tot_tok = p_tok + c_tok
        latency = tokens_info.get("latency", 0.0)

        footer_text = f"⚡ Tokens: {tot_tok} (Prompt: {p_tok} | Gen: {c_tok}) • Latency: {latency}s • Model: {model_name}"

        for idx, chunk in enumerate(chunks):
            title = f"💬 Response (Part {idx+1}/{len(chunks)})" if len(chunks) > 1 else None
            
            embed = discord.Embed(
                title=title,
                description=chunk,
                color=COLOR_NVIDIA_GREEN,
                timestamp=datetime.datetime.now(datetime.timezone.utc)
            )

            if idx == 0:
                # Truncate user query if long
                query_display = user_query if len(user_query) <= 200 else user_query[:197] + "..."
                embed.set_author(name=f"Query: {query_display}")

            # Add token usage metrics footer to final embed
            if idx == len(chunks) - 1:
                embed.set_footer(text=footer_text)

            embeds.append(embed)

        return embeds

    @staticmethod
    def build_image_embed(
        prompt: str,
        model_name: str,
        latency: float,
        enhanced_prompt: Optional[str] = None
    ) -> discord.Embed:
        """Builds a Discord Embed for generated AI images."""
        embed = discord.Embed(
            title="🎨 AI Image Generated",
            color=COLOR_DARK_PURPLE,
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        )
        embed.add_field(name="Prompt", value=f"*{prompt}*", inline=False)
        if enhanced_prompt and enhanced_prompt != prompt:
            embed.add_field(name="✨ Enhanced Prompt (NVIDIA Skill)", value=f"*{enhanced_prompt[:500]}*", inline=False)
        
        embed.set_footer(text=f"⚡ Model: {model_name} • Latency: {latency}s • NVIDIA NIM Visual AI")
        return embed



    @staticmethod
    def build_error_embed(title: str, description: str) -> discord.Embed:
        """Builds a standard red error embed."""
        embed = discord.Embed(
            title=f"❌ {title}",
            description=description,
            color=COLOR_ERROR_RED,
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        )
        embed.set_footer(text="Antigravity Discord AI • Error Handler")
        return embed
