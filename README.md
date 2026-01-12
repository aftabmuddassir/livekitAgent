# LiveKit Voice Agent 

This is a real-time voice AI agent that you can actually talk to. It listens, understands, responds, and can even call custom functions all in real-time with low latency.

## What Does It Do?

Think of it as having a conversation with an AI assistant, but through voice instead of text. You speak, it processes what you said, thinks about it, and speaks back. It feels pretty natural.

## Quick Start

### we'll Need

- Python 3.9 or newer
- API keys from:
  - [OpenAI](https://platform.openai.com/) (for the brain and voice)
  - [Deepgram](https://deepgram.com/) (for understanding speech)
  - [LiveKit Cloud](https://cloud.livekit.io/) (for connecting everything)

### Getting It Running

1. **Install UV** (a fast Python package manager):
   ```bash
   # Windows
   winget install astral-sh.uv
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Set up your API keys:**
   - Copy `.env.example` to `.env`
   - Fill in your actual API keys (get them from the links above)

4. **Download the AI models:**
   ```bash
   uv run python livekit_basic_agent.py download-files
   ```

5. **Talk to your agent:**
   ```bash
   uv run python livekit_basic_agent.py console
   ```

Start talking and the agent will respond.



### The Main Files

**`livekit_basic_agent.py`** - The simplest version. Great for getting started.
- Has one example tool: asks for current date/time
- Clean, minimal code
- Perfect for learning how it all works

**`livekit_mcp_agent.py`** - The full-featured version.
- Multiple example tools
- Logging and event handling
- Ready to extend with your own features

### How It Works

```
You speak → Deepgram converts to text → GPT-4o thinks and responds
→ OpenAI speaks the response → You hear the answer
```


## Try These Questions

- "Hello! What can you do?"
- "What's the current date and time?"
- "Tell me a joke"
- "What day of the week is it?"

## Adding Your Own Features

Want to teach it new tricks? It's easier than you think:

```python
@function_tool
async def your_custom_function(self, context: RunContext) -> str:
    """Describe what this does."""
    # Your code here
    return "Your response"
```

The agent will automatically know when to call your function based on what the user says!

## Real-World Uses

This same pattern can be used for:
- **Customer support** - Answer questions about your products
- **Voice search** - Search through company documents
- **Phone systems** - Replace those annoying "press 1 for..." menus
- **Accessibility** - Voice interfaces for apps
- **Education** - Interactive tutors that actually talk to you

## Tech Stack

Built with tools:
- **LiveKit** - Handles the real-time audio magic (open source)
- **OpenAI GPT-4o** - The brain behind the responses
- **Deepgram** - Incredibly fast speech recognition
- **Silero VAD** - Knows when you're speaking vs just background noise
- **Python + UV** - Fast, modern Python development
