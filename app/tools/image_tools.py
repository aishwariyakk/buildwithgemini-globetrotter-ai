"""
Image generation tools for GlobeTrotter AI.
Generates travel destination artwork using gemini-3.1-flash-lite-image,
saves it to ADK ToolContext artifacts, and uploads to public Google Cloud Storage.
"""

import uuid
from typing import Any
from google import genai
from google.genai import types
from google.cloud import storage
from google.adk.tools import ToolContext

# Hardcoded public GCS bucket name and GCP project ID (required)
GCS_BUCKET_NAME = "globetrotter-ai-media-qwiklabs-gcp-03-4d70f29521bc"
GCP_PROJECT_ID = "qwiklabs-gcp-03-4d70f29521bc"


def generate_destination_image(
    prompt: str,
    destination_name: str,
    tool_context: ToolContext,
) -> dict[str, Any]:
    """Generates a custom travel postcard or visual highlight image for a destination spot.

    Args:
        prompt: Description of the scene or landmark to illustrate (e.g. 'Eiffel Tower at sunset with warm evening light').
        destination_name: Name of the landmark or city (e.g. 'Eiffel Tower', 'Rome Colosseum').
        tool_context: ADK tool execution context for saving artifacts.

    Returns:
        A dictionary containing the destination name, artifact status, and public GCS web URL of the generated image.
    """
    # 1. Initialize GenAI client with global location for gemini-3.1-flash-lite-image
    client = genai.Client(location="global")

    full_prompt = (
        f"A beautiful artistic travel postcard illustration of {destination_name}: {prompt}. "
        "Vibrant colors, detailed architectural design, inviting atmosphere."
    )

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite-image",
        contents=full_prompt,
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"],
        ),
    )

    image_bytes = None
    mime_type = "image/png"

    if response.candidates and response.candidates[0].content:
        for part in response.candidates[0].content.parts:
            if part.inline_data:
                image_bytes = part.inline_data.data
                mime_type = part.inline_data.mime_type or "image/png"
                break

    if not image_bytes:
        return {
            "status": "error",
            "message": f"Failed to generate image for {destination_name}.",
        }

    ext = "jpg" if "jpeg" in mime_type else "png"
    unique_id = str(uuid.uuid4())[:8]
    sanitized_name = destination_name.lower().replace(" ", "-").replace("'", "")
    filename = f"{sanitized_name}-{unique_id}.{ext}"

    # (1) Save artifact for Playground Artifacts panel
    artifact_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
    tool_context.save_artifact(filename=filename, artifact=artifact_part)

    # (2) Upload image bytes directly to public GCS bucket
    storage_client = storage.Client(project=GCP_PROJECT_ID)
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(filename)
    blob.upload_from_string(image_bytes, content_type=mime_type)

    public_url = f"https://storage.googleapis.com/{GCS_BUCKET_NAME}/{filename}"

    return {
        "status": "success",
        "destination_name": destination_name,
        "artifact_filename": filename,
        "public_image_url": public_url,
        "message": f"Generated postcard image for {destination_name} successfully.",
    }
