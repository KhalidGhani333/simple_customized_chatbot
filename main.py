from agents import Agent , Runner , OpenAIChatCompletionsModel ,AsyncOpenAI ,set_tracing_disabled
import os
from dotenv import load_dotenv
from agents.run import RunConfig
import chainlit as cl

# Disable tracing
set_tracing_disabled(disabled=True)

# Load environment variables
load_dotenv()

# Load Gemini API key
API_KEY = os.environ.get("GEMINI_API_KEY")

# Create external client
external_client = AsyncOpenAI(
    api_key = API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Define the model and configuration
model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    openai_client = external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client
)

# Create the agent
agent = Agent(name="Assistant",instructions="you are a helpful assistant")


# Chainlit message handler
@cl.on_chat_start
async def start_chat():
    await cl.Message(content="👋 Hello! How Can I Help You Today?").send()

@cl.on_message
async def handle_message(message: cl.Message):
    user_input = message.content

  # Call the agent to get a response
    result = await Runner.run(agent, user_input, run_config=config)

 # Send the result back to the user
    await cl.Message(content=result.final_output).send()