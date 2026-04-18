from memory.store import MemoryStore
from agents.planner import PlannerAgent
from agents.executor import ExecutorAgent

class TestAutomationPipeline:
    def __init__(self):
        self.memory = MemoryStore()
        self.planner = PlannerAgent(self.memory)
        self.executor = ExecutorAgent()

    def run(self, ticket_id: str, progress_callback=None):
        if progress_callback:
            progress_callback("Planner Agent: Consulting Memory & Building Workflow...")
            
        plan_result = self.planner.plan_workflow(ticket_id)
        
        if plan_result["status"] == "CACHED":
            if progress_callback:
                progress_callback("Planner Agent: Found previous execution in Memory!")
            return plan_result["data"], True # True indicates it was cached
            
        if progress_callback:
            progress_callback("Planner Agent: Generated new execution plan.")
            
        final_data = self.executor.execute_plan(
            ticket_id, 
            plan_result["plan"], 
            progress_callback
        )
        
        if progress_callback:
            progress_callback("Saving execution results to Memory...")
            
        self.memory.save_execution(ticket_id, final_data)
        
        return final_data, False # False indicates it was freshly generated
