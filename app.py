import streamlit as st
import requests

# Backend URL (local FastAPI)
BACKEND_URL = "http://127.0.0.1:8000/submit-job"

st.set_page_config(page_title="OpenGradient Demo", page_icon="🚀", layout="centered")

st.title("OpenGradient Demo 🚀")
st.write("This app connects to the FastAPI backend for distributed GPU + TEE execution.")

# Input box
user_input: str = st.text_input("Enter a job input:", "")

# Submit button
if st.button("Submit Job"):
    if user_input.strip() == "":
        st.warning("⚠️ Please enter some input first.")
    else:
        try:
            response = requests.post(
                BACKEND_URL,
                json={"input": user_input},
                headers={"accept": "application/json"}
            )
            if response.status_code == 200:
                data = response.json()
                st.success("✅ Job executed successfully!")
                st.markdown(f"**Node Selected:** :blue[{data['result'].split('on ')[-1]}]")
                st.json(data)
            else:
                st.error(f"❌ Backend error: {response.status_code}")
        except Exception as e:
            st.error(f"⚠️ Could not connect to backend: {e}")
