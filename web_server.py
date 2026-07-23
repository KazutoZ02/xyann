import asyncio
import os
import time
import aiohttp
from aiohttp import web
import config

start_timestamp = time.time()

async def handle_health_check(request: web.Request) -> web.Response:
    """Returns 200 OK health status for Render and UptimeRobot pings."""
    uptime_seconds = int(time.time() - start_timestamp)
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    data = {
        "status": "online",
        "service": "NVIDIA NIM Discord AI Bot",
        "uptime": f"{hours}h {minutes}m {seconds}s",
        "default_model": config.DEFAULT_MODEL_KEY,
        "render_url": config.RENDER_URL or "Not Configured"
    }
    return web.json_response(data)

async def start_web_server():
    """Launches lightweight aiohttp web server asynchronously on port config.PORT."""
    app = web.Application()
    app.router.add_get('/', handle_health_check)
    app.router.add_get('/health', handle_health_check)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', config.PORT)
    await site.start()
    print(f"✅ Web Health Server listening on 0.0.0.0:{config.PORT} (Render Free Tier Ready)")

async def auto_ping_task():
    """Background task to self-ping RENDER_URL every 5 minutes to prevent Render spin-down."""
    await asyncio.sleep(15)  # Initial startup delay
    while True:
        url = config.RENDER_URL
        if url:
            if not url.startswith("http"):
                url = f"https://{url}"
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, timeout=10) as resp:
                        print(f"🔄 Auto-Ping sent to {url} (Status: {resp.status})")
            except Exception as e:
                print(f"⚠️ Auto-Ping failed to {url}: {str(e)}")
        else:
            print("ℹ️ RENDER_URL is not set. Use UptimeRobot or set RENDER_URL in .env to enable self-ping.")
            
        # Ping every 5 minutes (300 seconds)
        await asyncio.sleep(300)
