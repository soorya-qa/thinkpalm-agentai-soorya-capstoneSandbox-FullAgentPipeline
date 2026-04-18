from tools.jira_tool import JiraTool
from tools.llm_tool import LLMTool

class ExecutorAgent:
    """
    Executes the steps determined by the Planner Agent.
    """
    def __init__(self):
        self.jira_tool = JiraTool()
        self.llm_tool = LLMTool()

    def execute_plan(self, ticket_id: str, plan: list, progress_callback=None):
        results = {}
        
        for step in plan:
            if progress_callback:
                progress_callback(f"Executing step: {step}")
                
            if step == "FETCH_JIRA":
                results["jira_story"] = self.jira_tool.fetch_story(ticket_id)
            elif step == "GENERATE_BBD":
                if "jira_story" not in results:
                    raise ValueError("Cannot generate BDD without fetching JIRA story first.")
                results["bdd_cases"] = self.llm_tool.generate_test_cases(results["jira_story"])
            elif step == "GENERATE_CODE":
                if "bdd_cases" not in results:
                    raise ValueError("Cannot generate code without BDD cases.")
                results["code_scripts"] = self.llm_tool.generate_code(results["bdd_cases"])
            elif step == "ANALYZE_COVERAGE":
                if "jira_story" not in results or "bdd_cases" not in results:
                    raise ValueError("Cannot analyze coverage without JIRA story and BDD cases.")
                results["coverage_report"] = self.llm_tool.analyze_coverage(
                    results["jira_story"], 
                    results["bdd_cases"]
                )
        
        return results
