import os
import time
from google import genai
from google.genai.errors import APIError


def generate_chapter_draft(book_title, book_subtitle, chapter_title):
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        return "Error: GEMINI_API_KEY is missing in your Render Environment Variables."

    try:
        client = genai.Client(api_key=api_key)
        prompt = (
            f"You are an expert eBook ghostwriter. Write a well-structured, engaging chapter "
            f"for an eBook titled '{book_title}' ({book_subtitle}).\n"
            f"Chapter Title: '{chapter_title}'.\n"
            f"Write around 300-500 words with clear paragraphs and practical insights. "
            f"Return only the chapter body text without repeating the title."
        )

        # Use only active Gemini 3 text-generation models (never image or TTS models)
        models_to_try = [
            "gemini-3.8-flash",
            "gemini-3.6-flash",
            "gemini-3.5-flash-lite",
            "gemini-3.1-flash-lite",
        ]

        last_error = ""
        for model_name in models_to_try:
            for attempt in range(2):
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=prompt,
                    )
                    return response.text
                except APIError as e:
                    last_error = f"{model_name} ({e.code})"
                    # If busy (503) or rate-limited (429), pause briefly and retry or move to next model
                    if e.code in (429, 503):
                        if attempt == 0:
                            time.sleep(2)
                            continue
                        break
                    # If model isn't enabled on your tier (404/400), skip immediately
                    if e.code in (400, 404):
                        break
                    return f"AI Generation Error ({e.code}): {e.message}"

        return f"AI Generation Error: All text models are currently busy ({last_error}). Please wait 30 seconds and try again."

    except Exception as e:
        return f"AI Generation Error: {str(e)}"
