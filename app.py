import streamlit as st
from src.generate_explanation import generate_explanation
from src.generate_advice import generate_parenting_advice


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
        "Umfang der Erklärung:", ["kurz", "mittel", "ausführlich"], key="length"
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
    """UI und Logik für die Eltern-Beratung."""
    st.header("Eltern-Berater-Bot")

    question = st.text_input("Welche Erziehungsfrage hast du?", key="question")
    child_age = st.number_input(
        "Alter deines Kindes (in Jahren):", min_value=0, max_value=18, value=6, key="child_age"
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
        key="parenting_style",
    )

    if st.button("Beratung erhalten", key="advice_btn"):
        advice = generate_parenting_advice(question, child_age, parenting_style)
        st.subheader("Beratung")
        st.write(advice)


def main():
    st.set_page_config(page_title="Eltern-AI")
    st.title("Eltern-AI")

    tab_explain, tab_advice = st.tabs(["Erklärungs-Funktion", "Beratungs-Funktion"])

    with tab_explain:
        explanation_tab()

    with tab_advice:
        advice_tab()


if __name__ == "__main__":
    main()
