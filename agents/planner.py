from memory.store import MemoryStore

class PlannerAgent:
    """
    Decides the workflow for the testing pipeline.
    Checks memory to see if execution can be reused.
    """
    def __init__(self, memory_store: MemoryStore):
        self.memory = memory_store

    def plan_workflow(self, ticket_id: str):
        # Check memory first
        past_execution = self.memory.get_execution(ticket_id)
        if past_execution:
            return {
                "status": "CACHED",
                "plan": [],
                "data": past_execution["data"]
            }
        
        # If no memory, generate the standard plan
        return {
            "status": "NEW",
            "plan": [
                "FETCH_JIRA",
                "GENERATE_BBD",
                "GENERATE_CODE",
                "ANALYZE_COVERAGE"
            ],
            "data": {}
        }
