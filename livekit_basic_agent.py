"""
LiveKit Basic Voice Agent
A minimal LiveKit voice agent with essential components.
"""

import os
from datetime import datetime

from dotenv import load_dotenv
from livekit import agents
from livekit.agents import Agent, AgentSession, RunContext, function_tool
from livekit.plugins import deepgram, openai, silero

# Load environment variables
load_dotenv()


class Assistant(Agent):
    """Basic voice assistant agent."""

    def __init__(self):
        super().__init__(
            instructions="""You are a helpful voice assistant powered by LiveKit.
            Your interface with users will be voice-based.
            Keep your responses concise and conversational.
            You have access to tools that you can use to help users.
            Avoid using complex formatting, emojis, or symbols in your responses."""
        )

    @function_tool
    async def get_current_date_and_time(self, context: RunContext) -> str:
        """Get the current date and time."""
        current_time = datetime.now()
        formatted_time = current_time.strftime("%A, %B %d, %Y at %I:%M %p")
        return f"The current date and time is {formatted_time}"


async def entrypoint(ctx: agents.JobContext):
    """Entry point for the agent."""

    # Configure the voice pipeline
    session = AgentSession(
        stt=deepgram.STT(model="nova-2"),
        llm=openai.LLM(model=os.getenv("LLM_CHOICE", "gpt-4o-mini")),
        tts=openai.TTS(voice="alloy"),
        vad=silero.VAD.load(),
    )

    # Start the session
    await session.start(
        room=ctx.room,
        agent=Assistant()
    )

    # Generate initial greeting
    await session.generate_reply(
        instructions="Greet the user and offer your assistance."
    )


if __name__ == "__main__":
    # Run the agent
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
