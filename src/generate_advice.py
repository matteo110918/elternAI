from openai import OpenAI
from dotenv import load_dotenv
import os

# .env-Datei laden
load_dotenv()

# OpenAI-Client initialisieren
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def generate_parenting_advice(question: str, child_age: int, style: str) -> str:
    """Erstellt eine Erziehungsberatung."""
    system_msg = (
        "Du bist eine erfahrene pädagogische Fachkraft und beantwortest einfühlsam "
        "und fundiert Fragen zur Kindererziehung. Berücksichtige den angegebenen "
        "Erziehungsstil und das Alter des Kindes."
    )

    user_prompt = (
        f"Das Kind ist {child_age} Jahre alt und der bevorzugte Erziehungsstil ist '{style}'. "
        f"Frage: {question}"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            max_tokens=800,
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"❌ Fehler beim Abrufen der Beratung: {str(e)}"
