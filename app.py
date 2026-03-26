import streamlit as st
import pandas as pd
from main import gpu_node, tee_node, distributed_compute

# Page setup
st.set_page_config(page_title="OpenGradient Demo 🚀", page_icon="💻", layout="wide")

# Sidebar controls
st.sidebar.title("⚙️ Settings")
gpu_choice = st.sidebar.selectbox("Choose GPU node:", 
                                  ["Random", "GPU-Node-1", "GPU-Node-2", "GPU-Node-3"])
st.sidebar.info("Pick a GPU node or leave it random.")

# Main title
st.title("💻 OpenGradient Demo 🚀")
st.markdown("### Simulated Distributed GPU + TEE Execution")

# Job history
if "history" not in st.session_state:
    st.session_state["history"] = []

# Input area
user_input = st.text_input("📝 Enter a job input:")

# Submit button
if st.button("🚀 Submit Job"):
    if user_input.strip() == "":
        st.warning("⚠️ Please enter a job input.")
    else:
        # Run backend logic
        if gpu_choice == "Random":
            gpu_result = distributed_compute(user_input)
        else:
            gpu_result = gpu_node(user_input, gpu_choice)

        verification = tee_node(gpu_result)

        # Save to history
        st.session_state["history"].append({
            "input": user_input,
            "result": gpu_result,
            "verified": verification["verified"],
            "hash": verification["verification_hash"]
        })

# Display results
if st.session_state["history"]:
    st.subheader("📜 Job History")
    for job in reversed(st.session_state["history"]):
        st.success(f"✅ Input: {job['input']}")
        st.info(f"💡 Result: {job['result']}")
        st.write(f"🔒 Verified: {job['verified']}")
        st.code(f"🔑 Verification Hash: {job['hash']}")
        st.markdown("---")

    # Convert history to DataFrame
    df = pd.DataFrame(st.session_state["history"])

    # Download button
    st.download_button(
        label="⬇️ Download Job History as CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="job_history.csv",
        mime="text/csv"
    )

    # Clear history button
    if st.button("🗑️ Clear History"):
        st.session_state["history"] = []
        st.success("History cleared successfully!")
