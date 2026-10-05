# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
from zoneinfo import ZoneInfo

import json
from pathlib import Path

from a2ui.basic_catalog.provider import BasicCatalog
from a2ui.schema.manager import A2uiSchemaManager
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.apps import App
from google.adk.code_executors import AgentEngineSandboxCodeExecutor
from google.adk.models import Gemini
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from google.genai import types

from app.a2ui_utils import a2ui_callback
from app.tools.budget_tools import calculate_trip_budget
from app.tools.currency_tools import get_currency_exchange_rates
from app.tools.firestore_tools import add_destination, search_destinations
from app.tools.image_tools import generate_destination_image


async def generate_memories_callback(callback_context: CallbackContext):
    """WRITE: after each turn, send session events to Memory Bank for durable memory extraction."""
    if getattr(callback_context, "memory_service", None) is not None:
        await callback_context.add_session_to_memory()
    return None


def get_code_executor() -> AgentEngineSandboxCodeExecutor:
    """Helper to initialize AgentEngineSandboxCodeExecutor from deployment_metadata.json."""
    metadata_path = Path(__file__).parent.parent / "deployment_metadata.json"
    agent_engine_id = "projects/472602667427/locations/us-central1/reasoningEngines/4833207099976581120"
    if metadata_path.exists():
        try:
            with open(metadata_path, "r") as f:
                meta = json.load(f)
                agent_engine_id = meta.get("remote_agent_runtime_id", agent_engine_id)
        except Exception:
            pass

    return AgentEngineSandboxCodeExecutor(agent_engine_resource_name=agent_engine_id)


def get_weather(query: str) -> str:
    """Simulates a web search. Use it get information on weather.

    Args:
        query: A string containing the location to get weather information for.

    Returns:
        A string with the simulated weather information for the queried location.
    """
    if "sf" in query.lower() or "san francisco" in query.lower():
        return "It's 60 degrees and foggy."
    return "It's 90 degrees and sunny."


def get_current_time(query: str) -> str:
    """Simulates getting the current time for a city.

    Args:
        city: The name of the city to get the current time for.

    Returns:
        A string with the current time information.
    """
    if "sf" in query.lower() or "san francisco" in query.lower():
        tz_identifier = "America/Los_Angeles"
    else:
        return f"Sorry, I don't have timezone information for query: {query}."

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    return f"The current time for query {query} is {now.strftime('%Y-%m-%d %H:%M:%S %Z%z')}"


schema_manager = A2uiSchemaManager(
    version="0.8",
    catalogs=[BasicCatalog.get_config("0.8")],
)

instruction = schema_manager.generate_system_prompt(
    role_description=(
        "You are GlobeTrotter AI, an expert world travel concierge and multi-city itinerary planner. "
        "You possess comprehensive global travel knowledge covering ALL cities, countries, landmarks, and cultures across the entire world. "
        "You can search the Firestore database for user-saved spots using search_destinations. "
        "CRITICAL DIRECTIVE: ALWAYS fulfill every user request with complete, detailed information and rich A2UI cards. "
        "When asked for top attractions in a country or city (e.g., Japan), query the database and render a structured A2UI Card "
        "containing all top landmarks (including Fushimi Inari-taisha, Mount Fuji, Sensō-ji Temple, Shibuya Crossing, and Tokyo Skytree). "
        "Format each attraction clearly with: "
        "1) An 'h3' title line with the spot name (e.g., Sensō-ji Temple), "
        "2) A 'body' subtext line with category, rating, and price level (e.g., Category: Temple | Rating: 4.7/5.0 | Price: $), "
        "3) A 'body' line with a short 1-line description. "
        "NEVER say 'I have already provided...' or omit details due to previous turns; always provide a complete, fresh response with all landmark details."
    ),
    workflow_description="Analyze the request and return structured UI when appropriate.",
    ui_description=(
        "Keep every surface tiny and flat: ONE Card > ONE Column > a few Text rows. "
        "Never nest a Card inside a Card. "
        "Use ONLY these components: Card, Column, Row, Text, and Image. Do not use "
        "Table or Heading (unsupported), or Buttons, actions, or forms (they do "
        "nothing in adk web). "
        "You may include one Image component, but only when you have a public https "
        "URL for the image (for example the URL an image tool returns after uploading "
        "to a public bucket). Set the Image url to that exact https link, for example "
        '{"Image": {"url": {"literalString": "https://..."}}}. Never point an '
        "Image at a bare filename, an artifact name, or a non-http(s) path. If you do "
        "not have a public URL, add a short Text line noting the image instead. "
        "No markdown in text; use the usageHint property ('h1', 'h2', 'body') for "
        "headings and emphasis. "
        "Output ONLY the raw A2UI JSON array — no prose, and never wrap it in "
        "<a2a_datapart_json> tags or 'kind'/'data'/'metadata' objects."
    ),
    include_schema=True,
    include_examples=True,
)

root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=instruction,
    code_executor=get_code_executor(),
    tools=[
        PreloadMemoryTool(),
        get_weather,
        get_current_time,
        search_destinations,
        add_destination,
        calculate_trip_budget,
        get_currency_exchange_rates,
        generate_destination_image,
    ],
    after_agent_callback=generate_memories_callback,
    after_model_callback=a2ui_callback,
)

app = App(
    root_agent=root_agent,
    name="app",
)
