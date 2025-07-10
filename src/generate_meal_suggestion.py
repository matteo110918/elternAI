from typing import List, Optional

from openai import OpenAI
from dotenv import load_dotenv
import os

# .env-Datei laden
load_dotenv()

# OpenAI-Client initialisieren
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def generate_meal_suggestion(
    age: int,
    diet: str,
    portions: int,
    available_foods: Optional[List[str]] = None,
) -> str:
    """Generiert einen Essensvorschlag unter Berücksichtigung der Vorgaben.

    :param age: Alter des Kindes in Jahren.
    :param diet: Ernährungsstil (z. B. "Vegetarisch").
    :param portions: Anzahl der Portionen.
    :param available_foods: Liste vorhandener Lebensmittel.
    :return: Antworttext vom Sprachmodell.
    """

    available_text = (
        f" Folgende Lebensmittel sind bereits vorhanden: {', '.join(available_foods)}." 
        if available_foods else ""
    )

    system_msg = (
        "Du bist ein erfahrener Koch, der gesunde Mahlzeiten für Kinder vorschlägt. "
        "Berücksichtige Alter, Ernährungsstil und Portionsanzahl."
    )

    user_prompt = (
        f"Das Kind ist {age} Jahre alt. "
        f"Der Ernährungsstil ist '{diet}'. "
        f"Bitte schlage ein Gericht für {portions} Portionen vor." + available_text
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
        return f"❌ Fehler beim Abrufen des Essensvorschlags: {str(e)}"
