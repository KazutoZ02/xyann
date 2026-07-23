<<<<<<< HEAD
# xyann
=======
# 🚀 NVIDIA NIM Discord AI Bot (Render Free Tier 24/7 Ready)

A feature-rich, high-performance Discord AI bot in Python powered by **NVIDIA NIM API** set to max effort inference. Runs 24/7 on **Render's Free Tier**, operates in Direct Messages (DMs), responds using beautifully styled Discord Embeds, includes a dropdown model switcher, AI Image Generation, and GitHub integration for repo creation and code commits.

---

## ✨ Features

- 💬 **DM Chat & Embed Slicing**: Chat 1-on-1 with the bot in DMs. All responses format into rich Discord Embeds with syntax highlighting, token metrics, and automatic chunking (>4000 char handling).
- 🎛️ **Dropdown Model Switcher (`/model`)**: Switch models on-the-fly via an interactive Discord select menu:
  - **DeepSeek V4 Pro** (`deepseek-ai/deepseek-r1`)
  - **DeepSeek V4 Flash** (`deepseek-ai/deepseek-v3`)
  - **Nemotron 3 Ultra** (`nvidia/llama-3.1-nemotron-70b-instruct`)
  - **GLM 5.2 / GLM-4** (`thudm/glm-4-9b-chat`)
  - **Kimi K2.6** (`moonshotai/kimi-k1.5`)
  - **MiniMax M2.7 / M3** (`minimax/minimax-text-01`)
  - **Gemma 4 31B IT** (`google/gemma-2-27b-it`)
  - **Step 3.7 Flash** (`stepfun-ai/step-1-8k`)
  - **Laguna XS 2.1** (`laguna/xs-2.1`)
  - **Llama 3.3 70B** (`meta/llama-3.3-70b-instruct`)
- 🎨 **Text-to-Image Generation (`/imagine`)**: Generate photorealistic images powered by NVIDIA NIM **FLUX.1 Schnell** & **Stable Diffusion 3.5 Large** with automatic prompt expansion skill.
- ⚡ **Token & Latency Tracker (`/tokens`)**: Real-time token usage and latency embedded in every response footer.
- 🐙 **GitHub Integration (`/create_repo`, `/push_code`)**: Create public/private GitHub repositories & commit generated code files directly from Discord.
- 🌐 **Render 24/7 Keep-Alive**: Embedded `aiohttp` HTTP server (`GET /`) + background self-ping loop + UptimeRobot health check integration.

---

## 🛠️ Environment Variables Setup

Copy `.env.example` to `.env` and fill in your credentials:

```ini
DISCORD_TOKEN=your_discord_bot_token_here
NVIDIA_API_KEY=nvapi-your_nvidia_api_key_here
GITHUB_TOKEN=ghp_your_github_token_here
RENDER_URL=https://your-app-name.onrender.com
PORT=8080
```

### Key Prerequisites:
1. **Discord Token**: Create an application on [Discord Developer Portal](https://discord.com/developers/applications).
   - Go to **Bot** -> Enable **Message Content Intent** & **Direct Message** permissions.
   - Reset & copy the Bot Token.
2. **NVIDIA NIM API Key**: Generate your API key (`nvapi-...`) at [NVIDIA Build API Portal](https://build.nvidia.com/).
3. **GitHub PAT**: Generate a Personal Access Token with `repo` permissions at [GitHub Settings](https://github.com/settings/tokens).

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
   git commit -m "Initial commit of NVIDIA NIM Discord Bot"
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
   - `GITHUB_TOKEN`
   - `RENDER_URL` (Set this to your Render service URL, e.g. `https://nvidia-nim-bot.onrender.com`)

4. **UptimeRobot Setup (Optional Keep-Alive)**:
   - Go to [UptimeRobot.com](https://uptimerobot.com/).
   - Add new Monitor -> Type **HTTP(s)** -> Enter your Render URL (`https://your-app-name.onrender.com`).
   - Monitoring Interval: `5 minutes`.

---

## 🤖 Slash Commands Reference

| Command | Description |
| :--- | :--- |
| `/model` | Open dropdown menu to switch active NVIDIA NIM model |
| `/imagine <prompt>` | Generate photorealistic AI image via FLUX.1 / SD3.5 |
| `/create_repo <name>` | Create a new GitHub repository |
| `/push_code <repo> <path> <code>` | Commit and push code snippet directly to GitHub |
| `/tokens` | View accumulated token consumption & API stats |
| `/clear` | Reset current DM conversation context |
| `/help` | Display features and usage overview |

---

## 📜 License

MIT License. Built with `discord.py`, `aiohttp`, `PyGithub`, and NVIDIA NIM API.
>>>>>>> 7282557 (Initial commit: NVIDIA NIM Discord AI Bot with Render Keep-Alive and GitHub tools)
