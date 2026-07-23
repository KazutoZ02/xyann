# 🚀 Antigravity Discord AI Bot (Render Free Tier 24/7 Ready)

A feature-rich, high-performance Discord AI bot in Python powered by a dynamic multi-provider routing system (NVIDIA NIM, OpenRouter, and Nara). Runs 24/7 on **Render's Free Tier**, operates in server chat (via @mentions) and Direct Messages (DMs), responds using beautifully styled Discord Embeds, includes a categorized dropdown model switcher, and AI Image Generation.

---

## ✨ Features

- 💬 **Server & DM Chat**: Chat 1-on-1 with the bot in DMs or @mention it in any server channel. All responses format into rich Discord Embeds with syntax highlighting, token metrics, and automatic chunking (>4000 char handling).
- 🎛️ **Categorized Dropdown Model Switcher (`/model`)**: Switch models on-the-fly via an interactive Discord select menu organized by coding tasks:
  - **UI/UX Models**: Agnes 2.0 Flash, Gemma 4 26B (Vision)
  - **Frontend Models**: North Mini Code, Mistral Medium 3.5, Gemma 4 31B
  - **Backend Models**: Laguna S 2.1, Laguna M.1, Laguna XS 2.1, GPT-OSS 20B
  - **Full Stack Models**: Nemotron 3 Ultra, Nemotron 3 Super, Mistral Large, Qwen 2.5 72B, Llama 3.3 70B, GLM 5.2 Free, Grok 4.5
  - **Image Models**: Nemotron Nano 12B VL, Nemotron 3 Nano Omni
  - **Chat Models**: Nemotron Content Safety
- 🎨 **Text-to-Image Generation (`/imagine`)**: Generate photorealistic images powered by NVIDIA NIM **FLUX.1 Schnell** & **Stable Diffusion 3.5 Large** with automatic prompt expansion skill.
- ⚡ **Token & Latency Tracker (`/tokens`)**: Real-time token usage and latency embedded in every response footer.
- 🌐 **Render 24/7 Keep-Alive**: Embedded `aiohttp` HTTP server (`GET /`) + background self-ping loop + UptimeRobot health check integration.
- 🧠 **Dynamic API Routing**: Automatically routes requests to NVIDIA, OpenRouter, or Nara behind the scenes based on the selected model.

---

## 🛠️ Environment Variables Setup

Copy `.env.example` to `.env` and fill in your credentials:

```ini
DISCORD_TOKEN=your_discord_bot_token_here
NVIDIA_API_KEY=your_nvidia_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
NARA_API_KEY=your_nara_api_key_here
RENDER_URL=https://your-app-name.onrender.com
PORT=8080
```

### Key Prerequisites:
1. **Discord Token**: Create an application on [Discord Developer Portal](https://discord.com/developers/applications).
   - Go to **Bot** -> Enable **Message Content Intent** & **Direct Message** permissions.
   - Reset & copy the Bot Token.
2. **API Keys**: Generate API keys for NVIDIA NIM, OpenRouter, and Nara to ensure all categorized models work smoothly.

---

## 💻 Local Execution

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Bot**:
   ```bash
   python bot.py
   ```

3. Test web server at `http://localhost:8080/` (returns health status JSON).

---

## 🌐 Deploying to Render Free Tier (24/7 Uptime)

1. **Push your code to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit of Antigravity Discord Bot"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main
   ```

2. **Create Web Service on Render**:
   - Log into [Render.com](https://render.com/).
   - Click **New +** -> **Web Service**.
   - Connect your GitHub repository.
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bot.py`
   - **Instance Type**: `Free`

3. **Add Environment Variables on Render**:
   Under **Environment**, add:
   - `DISCORD_TOKEN`
   - `NVIDIA_API_KEY`
   - `OPENROUTER_API_KEY`
   - `NARA_API_KEY`
   - `RENDER_URL` (Set this to your Render service URL, e.g. `https://antigravity-bot.onrender.com`)

4. **UptimeRobot Setup (Optional Keep-Alive)**:
   - Go to [UptimeRobot.com](https://uptimerobot.com/).
   - Add new Monitor -> Type **HTTP(s)** -> Enter your Render URL (`https://your-app-name.onrender.com`).
   - Monitoring Interval: `5 minutes`.

---

## 🤖 Slash Commands Reference

| Command | Description |
| :--- | :--- |
| `/model` | Open dropdown menu to switch active LLM models |
| `/imagine <prompt>` | Generate photorealistic AI image via FLUX.1 / SD3.5 |
| `/tokens` | View accumulated token consumption & API stats |
| `/clear` | Reset current DM conversation context |
| `/help` | Display features and usage overview |

---

## 📜 License

MIT License. Built with `discord.py` and `aiohttp`.
