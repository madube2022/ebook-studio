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

    # Use current Gemini 3 models so the fallback never hits a retired 2.5 model
    models_to_try = ["gemini-3.8-flash", "gemini-3.8-flash-lite", "gemini-3.8-pro"]

    for model_name in models_to_try:
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                )
                return response.text
            except APIError as e:
                # Retry if busy (503) or rate-limited (429)
                if e.code in (429, 503):
                    if attempt < 2:
                        time.sleep(2 ** attempt)  # Wait 1s, then 2s
                        continue
                    break  # Try the next model in the list
                # If a fallback model name isn't enabled on your key (404), skip to the next one
                if e.code == 404:
                    break
                return f"AI Generation Error: {e}"
            except Exception as e:
                return f"AI Generation Error: {e}"

    return "AI Generation Error: The AI models are experiencing heavy traffic right now. Please wait 30 seconds and click Generate again."
