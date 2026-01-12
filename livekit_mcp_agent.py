"""
LiveKit MCP Voice Agent
A full-featured LiveKit voice agent with MCP server integration.
"""

import logging
import os
from datetime import datetime

from dotenv import load_dotenv
from livekit import agents
from livekit.agents import Agent, AgentSession, RunContext, function_tool
from livekit.plugins import deepgram, openai, silero

# Load environment variables
load_dotenv()

# Configure logging
log_level = os.getenv("LOG_LEVEL", "INFO")
logging.basicConfig(level=getattr(logging, log_level))
logger = logging.getLogger("mcp-agent")


class Assistant(Agent):
    """Full-featured voice assistant with multiple tools."""

    def __init__(self):
        super().__init__(
            instructions="""You are a helpful and friendly voice assistant powered by LiveKit.
            Your interface with users will be voice-based, so keep responses natural and conversational.
            Be concise but thorough. You have access to various tools that you can use to help users.
            When using tools, explain what you're doing in a natural way.
            Always be helpful, accurate, and respectful.
            Avoid using complex formatting, emojis, or symbols in your responses."""
        )

    @function_tool
    async def get_current_date_and_time(self, context: RunContext) -> str:
        """Get the current date and time."""
        current_time = datetime.now()
        formatted_time = current_time.strftime("%A, %B %d, %Y at %I:%M %p")
        logger.info(f"Tool called: get_current_date_and_time()")
        return f"The current date and time is {formatted_time}"

    @function_tool
    async def get_weather(self, context: RunContext, location: str) -> str:
        """Get the weather for a given location.

        Args:
            location: The location to get weather for
        """
        logger.info(f"Tool called: get_weather(location={location})")
        # This is a placeholder - integrate with a real weather API
        return f"I don't have real-time weather data yet, but you asked about the weather in {location}."


async def entrypoint(ctx: agents.JobContext):
    """Entry point for the MCP-enabled agent."""
    logger.info(f"Starting MCP agent for room: {ctx.room.name}")

    # Configure the voice pipeline
    session = AgentSession(
        stt=deepgram.STT(model="nova-2"),
        llm=openai.LLM(model=os.getenv("LLM_CHOICE", "gpt-4o-mini")),
        tts=openai.TTS(voice="alloy"),
        vad=silero.VAD.load(),
        # Add MCP servers here when needed:
        # mcp_servers=[
        #     mcp.MCPServerHTTP(url="http://localhost:8089/mcp")
        # ]
    )

    # Start the session
    await session.start(
        room=ctx.room,
        agent=Assistant()
    )

    # Generate initial greeting
    await session.generate_reply(
        instructions="Greet the user warmly and ask how you can help."
    )

    logger.info("MCP agent initialized and ready")


if __name__ == "__main__":
    # Run the agent
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
