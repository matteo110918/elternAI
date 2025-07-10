import streamlit as st
from src.generate_explanation import generate_explanation
from src.generate_advice import generate_parenting_advice
from src.generate_meal_suggestion import generate_meal_suggestion





def explanation_tab():
    """UI und Logik für kindgerechte Erklärungen."""
    st.header("Kindgerechte Erklärungen")

    topic = st.text_input("Gib ein Thema ein:", "Wie funktioniert ein Auto?", key="topic")

    age_group = st.selectbox(
        "Alter des Kindes:",
        ["< 3 Jahre", "3–6 Jahre", "7–9 Jahre", "10–12 Jahre", "13+ Jahre"],
        key="age_group",
    )

    style = st.radio(
        "Erklärform:",
        ["normale Erklärung", "als Geschichte", "Frage-Antwort-Dialog"],
        key="style",
    )

    length = st.radio(
        "Umfang der Erklärung:",
        ["kurz", "mittel", "ausführlich"],
        key="length"
    )

    if st.button("Erklärung generieren", key="explain_btn"):
        explanation = generate_explanation(topic, age_group, style, length)
        st.subheader("Kindgerechte Erklärung")
        st.write(explanation)

        if st.button("🧘 Noch einfacher erklären", key="simpler_btn"):
            simpler = generate_explanation(topic, age_group, style, "kurz")
            st.subheader("Vereinfachte Erklärung")
            st.write(simpler)


def advice_tab():
    """UI und Logik für die Eltern-Beratung mit Chat-Verlauf."""
    st.header("Eltern-Berater-Bot")

    # Session-State initialisieren
    if "advice_history" not in st.session_state:
        st.session_state.advice_history = []
    if "advice_question" not in st.session_state:
        st.session_state.advice_question = ""
    if "clear_advice_input" not in st.session_state:
        st.session_state.clear_advice_input = False

    if st.session_state.clear_advice_input:
        st.session_state.advice_question = ""
        st.session_state.clear_advice_input = False

    # Eingaben: Alter und Stil
    child_age = st.number_input(
        "Alter deines Kindes (in Jahren):",
        min_value=0,
        max_value=18,
        value=6,
        key="child_age"
    )

    parenting_style = st.selectbox(
        "Bevorzugter Erziehungsstil:",
        [
            "Autoritär",
            "Demokratisch",
            "Laissez-Faire",
            "Montessori",
            "Situationsbedingt",
            "Sonstige",
        ],
        key="parenting_style"
    )

    # Chatverlauf anzeigen
    for msg in st.session_state.advice_history:
        role = "Du" if msg["role"] == "user" else "Berater"
        st.markdown(f"**{role}:** {msg['content']}")

    # Eingabefeld
    st.text_input("Deine Nachricht:", key="advice_question")

    # Button klickt auf aktuelle Session-Eingabe
    if st.button("Senden"):
        question = st.session_state.advice_question.strip()

        if question:
            response = generate_parenting_advice(
                question,
                child_age,
                parenting_style,
                st.session_state.advice_history,
            )

            st.session_state.advice_history.append({"role": "user", "content": question})
            st.session_state.advice_history.append({"role": "assistant", "content": response})

        st.session_state.clear_advice_input = True
        st.rerun()


def meal_tab():
    """UI und Logik für Essensvorschläge."""
    st.header("Essensvorschläge")

    age = st.number_input(
        "Alter deines Kindes (in Jahren):",
        min_value=0,
        max_value=18,
        value=6,
        key="meal_age",
    )

    diet = st.selectbox(
        "Ernährungsstil:",
        ["Omnivor", "Vegetarisch", "Vegan", "Glutenfrei", "Laktosefrei", "Sonstige"],
        key="meal_diet",
    )

    portions = st.number_input(
        "Anzahl der Portionen:",
        min_value=1,
        max_value=10,
        value=2,
        key="meal_portions",
    )

    foods_input = st.text_input(
        "Lebensmittel, die du zuhause hast (kommagetrennt):",
        key="meal_foods",
    )

    if st.button("Essensvorschlag generieren", key="meal_btn"):
        foods = [f.strip() for f in foods_input.split(",") if f.strip()] if foods_input else None
        suggestion = generate_meal_suggestion(age, diet, portions, foods)
        st.subheader("Vorgeschlagenes Gericht")
        st.write(suggestion)


def main():
    st.set_page_config(page_title="Eltern-AI")
    st.title("Eltern-AI")

    tab_explain, tab_advice, tab_meal = st.tabs([
        "Erklärungs-Funktion",
        "Beratungs-Funktion",
        "Essens-Vorschlag",
    ])

    with tab_explain:
        explanation_tab()

    with tab_advice:
        advice_tab()

    with tab_meal:
        meal_tab()


if __name__ == "__main__":
    main()
