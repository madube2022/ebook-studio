import os
import time
from google import genai
from google.genai.errors import APIError


def generate_chapter_draft(book_title, book_subtitle, chapter_title):
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        return "Error: GEMINI_API_KEY is missing in your Render Environment Variables."

    client = genai.Client(api_key=api_key)
    prompt = (
        f"You are an expert eBook ghostwriter. Write a well-structured, engaging chapter "
        f"for an eBook titled '{book_title}' ({book_subtitle}).\n"
        f"Chapter Title: '{chapter_title}'.\n"
        f"Write around 300-500 words with clear paragraphs and practical insights. "
        f"Return only the chapter body text without repeating the title."
    )

    # Try your primary model first, then fall back to stable models if busy
    models_to_try = ["gemini-3.8-flash", "gemini-2.5-flash", "gemini-2.5-flash-lite"]

    for model_name in models_to_try:
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                )
                return response.text
            except APIError as e:
                # 503 = High demand / overloaded; 429 = Rate limit
                if e.code in (429, 503):
                    if attempt < 2:
                        time.sleep(2 ** attempt)  # Wait 1s, then 2s before retrying
                        continue
                    # Move on to the next model in the list if all 3 attempts fail
                    break
                return f"AI Generation Error: {e}"
            except Exception as e:
                return f"AI Generation Error: {e}"

    return "AI Generation Error: All AI models are currently busy due to high demand. Please try again in a minute."
