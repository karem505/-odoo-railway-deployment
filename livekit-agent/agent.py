"""
LiveKit Voice Agent for Odoo Navigation
Handles voice commands in Arabic and English to navigate Odoo modules
"""

import asyncio
import json
import logging
import os
from urllib.parse import urlparse
from dotenv import load_dotenv

from livekit import rtc
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    JobProcess,
    WorkerOptions,
    cli,
    llm,
)
from livekit.agents.pipeline import VoicePipelineAgent
from livekit.plugins import openai, silero

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
LIVEKIT_URL = os.getenv("LIVEKIT_URL")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
FRONTEND_BASE_URL = os.getenv("ODOO_FRONTEND_URL", "http://localhost:8069")

# Load agent instructions
INSTRUCTIONS_FILE = os.path.join(os.path.dirname(__file__), "prompts", "agent_instructions.txt")

def load_instructions():
    """Load agent personality and instructions from file"""
    try:
        with open(INSTRUCTIONS_FILE, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        logger.warning(f"Instructions file not found: {INSTRUCTIONS_FILE}")
        return """You are a helpful voice assistant for Odoo ERP navigation.
You can help users navigate between different Odoo modules using voice commands in Arabic or English.
Be friendly, concise, and helpful."""


class OdooNavigationAgent:
    """Voice agent that handles Odoo navigation commands"""

    def __init__(self, ctx: JobContext):
        self.ctx = ctx
        self._room = None

    async def entrypoint(self):
        """Main entrypoint for the agent"""
        logger.info(f"Starting Odoo Navigation Agent")
        logger.info(f"Frontend URL: {FRONTEND_BASE_URL}")

        # Connect to the room
        await self.ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
        self._room = self.ctx.room

        # Load instructions
        instructions = load_instructions()

        # Create function context with navigation tools
        fnc_ctx = llm.FunctionContext()

        # Register navigation functions
        fnc_ctx.ai_callable()(self.navigate_to_sales)
        fnc_ctx.ai_callable()(self.navigate_to_crm)
        fnc_ctx.ai_callable()(self.navigate_to_inventory)
        fnc_ctx.ai_callable()(self.navigate_to_accounting)
        fnc_ctx.ai_callable()(self.navigate_to_purchases)
        fnc_ctx.ai_callable()(self.navigate_to_hr)
        fnc_ctx.ai_callable()(self.navigate_to_projects)
        fnc_ctx.ai_callable()(self.navigate_to_manufacturing)
        fnc_ctx.ai_callable()(self.go_home)
        fnc_ctx.ai_callable()(self.where_am_i)

        # Create the voice pipeline agent
        agent = VoicePipelineAgent(
            vad=silero.VAD.load(),
            stt=openai.STT(),
            llm=openai.LLM(model="gpt-4o"),
            tts=openai.TTS(),
            fnc_ctx=fnc_ctx,
            chat_ctx=llm.ChatContext().append(
                role="system",
                text=instructions,
            ),
        )

        # Start the agent
        agent.start(self.ctx.room)

        # Wait for participant to join
        participant = await self.ctx.wait_for_participant()
        logger.info(f"Participant joined: {participant.identity}")

        # Greet the user
        await agent.say("Hello! I'm your Odoo voice assistant. You can ask me to navigate to different modules.", allow_interruptions=True)

    # Navigation Functions

    async def navigate_to_sales(self):
        """Navigate to Sales module"""
        url = f"{FRONTEND_BASE_URL}/web#menu_id=sales.sale_menu_root"
        await self._send_navigation_url(url)
        return "Opening Sales module"

    async def navigate_to_crm(self):
        """Navigate to CRM/Customers module"""
        url = f"{FRONTEND_BASE_URL}/web#menu_id=crm.crm_menu_root"
        await self._send_navigation_url(url)
        return "Opening CRM module"

    async def navigate_to_inventory(self):
        """Navigate to Inventory/Stock module"""
        url = f"{FRONTEND_BASE_URL}/web#menu_id=stock.menu_stock_root"
        await self._send_navigation_url(url)
        return "Opening Inventory module"

    async def navigate_to_accounting(self):
        """Navigate to Accounting module"""
        url = f"{FRONTEND_BASE_URL}/web#menu_id=account.menu_finance"
        await self._send_navigation_url(url)
        return "Opening Accounting module"

    async def navigate_to_purchases(self):
        """Navigate to Purchases module"""
        url = f"{FRONTEND_BASE_URL}/web#menu_id=purchase.menu_purchase_root"
        await self._send_navigation_url(url)
        return "Opening Purchases module"

    async def navigate_to_hr(self):
        """Navigate to Human Resources module"""
        url = f"{FRONTEND_BASE_URL}/web#menu_id=hr.menu_hr_root"
        await self._send_navigation_url(url)
        return "Opening HR module"

    async def navigate_to_projects(self):
        """Navigate to Projects module"""
        url = f"{FRONTEND_BASE_URL}/web#menu_id=project.menu_main_pm"
        await self._send_navigation_url(url)
        return "Opening Projects module"

    async def navigate_to_manufacturing(self):
        """Navigate to Manufacturing/MRP module"""
        url = f"{FRONTEND_BASE_URL}/web#menu_id=mrp.menu_mrp_root"
        await self._send_navigation_url(url)
        return "Opening Manufacturing module"

    async def go_home(self):
        """Navigate to home/dashboard"""
        url = f"{FRONTEND_BASE_URL}/web"
        await self._send_navigation_url(url)
        return "Going to home page"

    async def where_am_i(self):
        """Tell user their current location - they need to inform you"""
        return "I need you to tell me where you are. What page or module are you currently viewing?"

    async def _send_navigation_url(self, url: str):
        """Helper to send navigation URL via data channel"""
        try:
            # Extract just the path part
            parsed = urlparse(url)
            pathname = parsed.fragment if parsed.fragment else parsed.path

            # Send via data channel
            navigation_data = {
                "type": "agent-navigation-url",
                "pathname": f"#{pathname}" if not pathname.startswith('#') else pathname
            }

            # Send to all participants in room
            if self._room:
                await self._room.local_participant.publish_data(
                    json.dumps(navigation_data).encode('utf-8'),
                    reliable=True
                )
                logger.info(f"Sent navigation command: {pathname}")
        except Exception as e:
            logger.error(f"Error sending navigation: {e}")


def prewarm(proc: JobProcess):
    """Prewarm function to load models before handling jobs"""
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext):
    """Job entrypoint that creates and runs the agent"""
    agent = OdooNavigationAgent(ctx)
    await agent.entrypoint()


if __name__ == "__main__":
    # Run the worker
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            prewarm_fnc=prewarm,
        ),
    )
