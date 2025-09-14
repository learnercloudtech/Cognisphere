import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from agents.meta_agent import MetaAgent

# 🎛️ Sidebar Controls
with st.sidebar:
    st.header("⚙️ Cognisphere Settings")
    selected_model = st.selectbox("LLM Model", ["llama3", "codellama"])
    max_depth = st.slider("Max Recursion Depth", 1, 5, 2)
    show_trace = st.checkbox("Show Task Ledger")

# 🧠 Page Setup
st.set_page_config(page_title="Cognisphere Dashboard", layout="wide")
st.title("🧠 Cognisphere Recursive Agentic System")

# 🔍 Task Input
task = st.text_input("Enter a high-level task for Cognisphere to solve:")

# 🚀 Run Agents
if st.button("Run Agents") and task:
    with st.spinner("Agents thinking..."):
        agent = MetaAgent(task)
        agent.max_depth = max_depth
        result = agent.execute()

    st.success("✅ Agent execution complete!")

    # 📈 Top Metrics
    col1, col2 = st.columns(2)
    col1.metric("🧠 Overall Quality Score", result["score"]["quality"])
    col2.caption(f"💬 Final Feedback: {result['score']['feedback']}")

    # 📋 Agent Outputs
    for subtask, details in result["context"].items():
        st.markdown("---")
        st.subheader(f"📌 Subtask: `{subtask}`")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("🔍 **ResearchAgent Output**")
            st.write(details["research"])
        with col2:
            st.markdown("📝 **SummarizerAgent Output**")
            st.write(details["summary"])

        eval_data = details["evaluation"]
        assign_data = details["assignment"]

        st.markdown(f"📊 **Evaluation Score**: `{eval_data['quality']}`")
        st.markdown(f"💬 **Feedback**: {eval_data['feedback']}")
        st.markdown(f"📋 **Assignment**: {assign_data['message']}")
        st.caption(f"🔧 Assigned Role: `{assign_data['assigned_role']}` | Status: `{assign_data['status']}`")

    # 📁 Task Ledger (Optional)
    if show_trace:
        st.markdown("---")
        st.subheader("📁 Task Ledger")
        for entry in agent.task_manager_agent.task_log:
            st.markdown(
                f"- `{entry['subtask']}` → `{entry['status']}` by `{entry['assigned_role']}` | Score: `{entry['quality']}`"
            )
