from typing import List, Dict, Optional

from openai import OpenAI
from dotenv import load_dotenv
import os

# .env-Datei laden
load_dotenv()

# OpenAI-Client initialisieren
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def generate_parenting_advice(
    question: str,
    child_age: int,
    style: str,
    history: Optional[List[Dict[str, str]]] = None,
) -> str:
    """Erstellt eine Erziehungsberatung und unterstützt einen Chat-Verlauf.

    :param question: Aktuelle Frage bzw. Nachricht der Nutzerin oder des Nutzers.
    :param child_age: Alter des Kindes in Jahren.
    :param style: Bevorzugter Erziehungsstil.
    :param history: Vorheriger Nachrichtenverlauf ohne System‑Nachricht.
    :return: Antworttext vom Sprachmodell.
    """
    system_msg = (
        "Du bist eine erfahrene pädagogische Fachkraft und beantwortest einfühlsam "
        "und fundiert Fragen zur Kindererziehung. Berücksichtige den angegebenen "
        "Erziehungsstil und das Alter des Kindes."
    )

    user_prompt = (
        f"Das Kind ist {child_age} Jahre alt und der bevorzugte Erziehungsstil ist '{style}'. "
        f"Frage: {question}"
    )

    messages = [{"role": "system", "content": system_msg}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": user_prompt})

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
            max_tokens=800,
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"❌ Fehler beim Abrufen der Beratung: {str(e)}"
