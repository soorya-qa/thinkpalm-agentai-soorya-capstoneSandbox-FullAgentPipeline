import os
from jira import JIRA

class JiraTool:
    def __init__(self):
        self.base_url = os.environ.get("JIRA_BASE_URL", os.environ.get("JIRA_PROJECT_URL"))
        self.email = os.environ.get("JIRA_EMAIL")
        self.api_key = os.environ.get("JIRA_API_KEY")
        
        if not all([self.base_url, self.email, self.api_key]):
            raise ValueError("Jira credentials missing in .env file")
            
        self.client = JIRA(server=self.base_url, basic_auth=(self.email, self.api_key))

    def fetch_story(self, ticket_id: str) -> str:
        try:
            issue = self.client.issue(ticket_id)
            summary = issue.fields.summary
            description = issue.fields.description or "No description provided."
            
            # Combine them for the LLM
            feature_text = f"Title: {summary}\n\nDescription:\n{description}"
            return feature_text
        except Exception as e:
            raise Exception(f"Failed to fetch Jira ticket {ticket_id}: {str(e)}")
