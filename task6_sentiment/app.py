import streamlit as st
import pickle

# Load trained model
with open("sentiment_model.pkl", "rb") as f:
    model = pickle.load(f)

vectorizer = model["vectorizer"]
classifier = model["classifier"]

st.set_page_config(
    page_title="Sentiment Analysis",
    page_icon="😊",
    layout="centered"
)

st.title("😊 AI Sentiment Analysis")
st.write("Analyze whether a sentence is Positive, Neutral or Negative.")

text = st.text_area(
    "Enter text",
    placeholder="Example: This phone is amazing!"
)

if st.button("Analyze Sentiment"):

    if text.strip() == "":
        st.warning("Please enter some text.")
    else:

        vector = vectorizer.transform([text])

        prediction = classifier.predict(vector)[0]

        probabilities = classifier.predict_proba(vector)[0]

        st.subheader("Prediction")

        if prediction == "positive":
            st.success("😊 Positive")

        elif prediction == "negative":
            st.error("☹️ Negative")

        else:
            st.info("😐 Neutral")

        st.subheader("Confidence")

        for label, score in zip(classifier.classes_, probabilities):
            st.progress(float(score))
            st.write(f"**{label.title()}** : {score:.2%}")
