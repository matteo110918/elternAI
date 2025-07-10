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
    child_ages: List[int],
    adult_count: int,
    diet: str,
    preference: Optional[str] = None,
    available_foods: Optional[List[str]] = None,
) -> str:
    """Generiert einen Essensvorschlag unter Berücksichtigung der Vorgaben.

    :param child_ages: Liste der Kinderalter in Jahren.
    :param adult_count: Anzahl der Erwachsenen.
    :param diet: Ernährungsstil (z. B. "Vegetarisch").
    :param preference: Wunschgericht oder bevorzugte Art von Mahlzeit.
    :param available_foods: Liste vorhandener Lebensmittel.
    :return: Antworttext vom Sprachmodell.
    """

    available_text = (
        f" Folgende Lebensmittel sind bereits vorhanden: {', '.join(available_foods)}."
        if available_foods
        else ""
    )

    system_msg = (
        "Du bist ein erfahrener Koch, der gesunde Mahlzeiten für Familien vorschlägt. "
        "Berücksichtige die Altersangaben der Kinder, die Anzahl der Erwachsenen und den Ernährungsstil."
    )

    child_description = (
        "keine Kinder"
        if not child_ages
        else f"{len(child_ages)} Kinder im Alter von {', '.join(map(str, child_ages))} Jahren"
    )

    pref_text = f" Bevorzugt sind Gerichte wie '{preference}'." if preference else ""

    user_prompt = (
        f"Es sind {child_description} und {adult_count} Erwachsene zu verköstigen. "
        f"Der Ernährungsstil ist '{diet}'."
        + pref_text +
        " Bitte schlage ein Gericht mit passenden Portionen vor." + available_text
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
