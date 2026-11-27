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

    # Start with your preferred model
    models_to_try = ["gemini-3.8-flash"]

    # Automatically discover any other text-generation Gemini models enabled on your key
    try:
        for m in client.models.list():
            name = m.name.replace("models/", "")
            if "gemini" in name and "embedding" not in name and "imagen" not in name:
                if name not in models_to_try:
                    models_to_try.append(name)
    except Exception:
        pass

    last_error = ""
    for model_name in models_to_try[:5]:  # Try up to 5 available models
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                )
                return response.text
            except APIError as e:
                last_error = f"{model_name}: {e}"
                if e.code in (429, 503):
                    if attempt < 2:
                        time.sleep(2 * (attempt + 1))  # Wait 2s, then 4s
                        continue
                    break  # Move to the next valid model
                if e.code in (400, 404):
                    break  # Skip unsupported/non-text models
                return f"AI Generation Error: {e}"
            except Exception as e:
                return f"AI Generation Error: {e}"

    return f"AI Generation Error: Servers are busy ({last_error}). Please try again shortly."
