from openai import OpenAI
from dotenv import load_dotenv
import os

# .env-Datei laden
load_dotenv()

# OpenAI-Client initialisieren
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def generate_explanation(topic: str, age_group: str, style: str, length: str) -> str:
    """
    Generiert eine kindgerechte Erklärung zu einem Thema anhand der Nutzerangaben.

    :param topic: Thema der Erklärung (z. B. "Was ist Strom?")
    :param age_group: Altersgruppe (z. B. "3–6 Jahre")
    :param style: Erklärstil (z. B. "als Geschichte")
    :param length: Umfang (kurz, mittel, ausführlich)
    :return: Antworttext vom Sprachmodell
    """
    system_msg = (
        "Du bist eine freundliche und pädagogisch geschulte AI, die kindgerechte Erklärungen erstellt. "
        "Sprich altersgerecht, empathisch und klar."
        "Beginne direkt mit der Erklärung - ohne Einleitung oder Floskeln."
    )

    user_prompt = (
        f"Erkläre bitte das Thema '{topic}' so, dass es ein Kind im Alter von {age_group} versteht. "
        f"Nutze die Erklärform '{style}'. "
        f"Der Umfang soll {length} sein. "
        f"Sprich freundlich, klar und kindgerecht."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"❌ Fehler beim Abrufen der Erklärung: {str(e)}"
