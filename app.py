import streamlit as st
from main import distributed_compute, tee_node

st.title("OpenGradient Demo 🚀")
st.write("Simulated distributed GPU + TEE execution")

# Input box
user_input = st.text_input("Enter a job input:")

# Button to submit
if st.button("Submit Job"):
    if user_input.strip() == "":
        st.warning("Please enter a job input.")
    else:
        # Run backend logic directly
        gpu_result = distributed_compute(user_input)
        verification = tee_node(gpu_result)

        # Show results
        st.success(f"Input: {user_input}")
        st.info(f"Result: {gpu_result}")
        st.write(f"Verified: {verification['verified']}")
        st.code(f"Verification Hash: {verification['verification_hash']}")
