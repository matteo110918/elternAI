import streamlit as st
from src.generate_explanation import generate_explanation

def get_user_inputs():
    st.title("Eltern-AI: Kindgerechte Erklärungen")

    topic = st.text_input("Gib ein Thema ein:", "Was ist der Tod?")

    age_group = st.selectbox("Alter des Kindes:",
                              ["< 3 Jahre", "3–6 Jahre", "7–9 Jahre", "10–12 Jahre", "13+ Jahre"])

    style = st.radio("Erklärform:",
                     ["normale Erklärung", "als Geschichte", "Frage-Antwort-Dialog"])

    length = st.radio("Umfang der Erklärung:",
                      ["kurz", "mittel", "ausführlich"])

    return topic, age_group, style, length

def show_explanation(topic: str, age_group: str, style: str, length: str):
    explanation = generate_explanation(topic, age_group, style, length)
    st.subheader("Kindgerechte Erklärung")
    st.write(explanation)

    if st.button("🔁 Noch einfacher erklären"):
        simpler = generate_explanation(topic, age_group, style, "kurz")
        st.subheader("Vereinfachte Erklärung")
        st.write(simpler)

def main():
    topic, age_group, style, length = get_user_inputs()

    if st.button("Erklärung generieren"):
        show_explanation(topic, age_group, style, length)

if __name__ == "__main__":
    main()