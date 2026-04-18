import streamlit as st
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Ensure parent directory is in path so we can import agents
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.pipeline import TestAutomationPipeline

def main():
    st.set_page_config(page_title="Agentic Test Automation Pipeline", layout="wide")
    
    st.title("🤖 AI-Powered Test Automation Assistant")
    st.markdown("A multi-agent system that reads JIRA stories and generates testing artifacts autonomously.")
    
    # Initialize session state for results if not present
    if "final_results" not in st.session_state:
        st.session_state.final_results = None
    if "is_cached" not in st.session_state:
        st.session_state.is_cached = False

    with st.sidebar:
        st.header("Configuration & Status")
        ticket_id = st.text_input("Enter JIRA Issue ID:", placeholder="e.g., PROJ-123")
        run_btn = st.button("Generate ", type="primary")
        
        st.divider()
        st.markdown("**Agents Online:**")
        st.markdown("- 🧠 **Planner Agent**")
        st.markdown("- ⚙️ **Executor Agent**")
        
        st.divider()
        st.markdown("**Tools Prepared:**")
        st.markdown("- 🎫 JIRA API Tool")
        st.markdown("- 💬 LLM Generator Tool")
        st.markdown("- 💾 JSON Memory Store")

    if run_btn:
        if not ticket_id:
            st.error("Please enter a valid JIRA Issue ID.")
            return
            
        st.session_state.final_results = None # Reset
        
        status_box = st.empty()
        
        def ui_callback(msg):
            status_box.info(f"⏳ {msg}")
            
        try:
            pipeline = TestAutomationPipeline()
            with st.spinner("Pipeline is running..."):
                results, cached = pipeline.run(ticket_id, progress_callback=ui_callback)
            
            st.session_state.final_results = results
            st.session_state.is_cached = cached
            
            if cached:
                status_box.success(f"✅ Retrieved past execution from Memory Store for {ticket_id}")
            else:
                status_box.success(f"✅ Pipeline completed successfully and saved to Memory for {ticket_id}!")
                
        except Exception as e:
            status_box.error(f"❌ Error during execution: {str(e)}")

    # Display results if available
    if st.session_state.final_results:
        res = st.session_state.final_results
        
        if st.session_state.is_cached:
            st.warning("ℹ️ *Displaying data loaded from memory, bypassing LLM generation.*")
            
        tab1, tab2, tab3, tab4 = st.tabs([
            "JIRA Story", "BDD Scenarios", "Automation Script", "Coverage Gap Report"
        ])
        
        with tab1:
            st.subheader("Feature Context extracted from JIRA")
            st.text_area("Story Data", res.get("jira_story", "N/A"), height=300, disabled=True)
            
        with tab2:
            st.subheader("Generated Gherkin Scenarios")
            st.code(res.get("bdd_cases", ""), language="gherkin")
            
        with tab3:
            st.subheader("Playwright Automation Code")
            st.code(res.get("code_scripts", ""), language="python")
            
        with tab4:
            st.subheader("Test Coverage Analytics")
            st.markdown(res.get("coverage_report", ""))

if __name__ == "__main__":
    main()
