import os
from openai import OpenAI

class LLMTool:
    def __init__(self):
        # Prefer Groq if key exists, otherwise try OpenAI
        groq_key = os.environ.get("GROQ_API_KEY")
        openai_key = os.environ.get("OPENAI_API_KEY")
        
        if groq_key:
            self.client = OpenAI(
                api_key=groq_key,
                base_url="https://api.groq.com/openai/v1"
            )
            self.model = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")
        elif openai_key:
            self.client = OpenAI(api_key=openai_key)
            self.model = "gpt-4o"
        else:
            raise ValueError("No valid GROQ_API_KEY or OPENAI_API_KEY found in .env")

    def _generate(self, system_instruction: str, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
        )
        return response.choices[0].message.content

    def generate_test_cases(self, feature_description: str) -> str:
        sys_inst = (
            "You are an expert QA Automation Engineer. "
            "Convert the provided feature description into structured Gherkin (BDD) format. "
            "Return only valid Gherkin text, no markdown styling around the text like ```gherkin."
        )
        prompt = f"Feature Description:\n{feature_description}"
        result = self._generate(sys_inst, prompt)
        return result.replace("```gherkin", "").replace("```", "").strip()

    def generate_code(self, gherkin_content: str) -> str:
        sys_inst = (
            "You are an SDET. Convert the given Gherkin feature into standard "
            "pytest-bdd and pytest-playwright Python scripts. "
            "For your imports, assume you have `pytest`, `pytest_bdd`, and `playwright.sync_api`. "
            "Only output the raw python code, no markdown wrappers like ```python."
        )
        prompt = f"Gherkin Feature:\n{gherkin_content}"
        result = self._generate(sys_inst, prompt)
        return result.replace("```python", "").replace("```", "").strip()

    def analyze_coverage(self, feature_description: str, gherkin_content: str) -> str:
        sys_inst = (
            "You are a Senior QA Manager. Review the original Feature Description and the "
            "generated Gherkin Scenarios. Identify what edge cases, negative tests, performance, "
            "or security aspects are missing from the Gherkin scenarios. Output a structured markdown report."
        )
        prompt = (
            f"Feature Description:\n{feature_description}\n\n"
            f"Generated Gherkin:\n{gherkin_content}"
        )
        return self._generate(sys_inst, prompt)
