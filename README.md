# thinkpalm-agentai-soorya-capstoneSandbox-FullAgentPipeline

# AI Test Automation Agent (Capstone Sandbox D8)

Name: Soorya M S  
Track: QA Automation  
Lab: Capstone Sandbox — Full Agent Pipeline (D8)  

Objective:
Build a complete end-to-end agentic pipeline aligned to the QA Automation track.

What This Project Does:
This project is an AI-powered test automation assistant that:
- Fetches user stories from JIRA
- Generates BDD/Gherkin test cases
- Creates Playwright automation scripts
- Identifies coverage gaps

Capstone Requirements Covered:
- Multi-agent system (Planner, Executor, Reviewer)
- Tool-calling (JIRA API, LLM)
- Memory storage (JSON-based)
- Working UI (Streamlit)
- End-to-end autonomous pipeline

Architecture:
- Planner Agent → decides workflow
- Executor Agent → calls tools
- Reviewer Agent → validates outputs

Tools Used:
- Python
- Gemini/OpenAI API
- Streamlit
- JIRA REST API

Project Structure:
- /src → source code
- /screenshots → output screenshots
- requirements.txt → dependencies
