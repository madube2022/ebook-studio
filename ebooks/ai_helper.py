import os
from google import genai


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

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"AI Generation Error: {e}"
