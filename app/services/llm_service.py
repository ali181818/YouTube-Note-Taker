import os
from litellm import completion
from app.config import OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY, DEFAULT_LLM, DEFAULT_PROMPT_TEMPLATE

class LLMService:
    def __init__(self, model=None):
        self.model = model or DEFAULT_LLM
        self._setup_api_keys()
    
    def _setup_api_keys(self):
        """Set up API keys based on the selected model"""
        if self.model == "OPENAI":
            os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
            self.model_name = "gpt-4"
        elif self.model == "ANTHROPIC":
            os.environ["ANTHROPIC_API_KEY"] = ANTHROPIC_API_KEY
            self.model_name = "claude-3-opus-20240229"
        else:  # Default to GEMINI
            os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY
            self.model_name = "gemini-pro"
            self.model = "GEMINI"
    
    def process_transcript(self, transcript, custom_prompt=None):
        """Process the transcript using an LLM and return the result"""
        # Prepare the prompt
        prompt = custom_prompt or DEFAULT_PROMPT_TEMPLATE
        formatted_prompt = prompt.format(transcript=transcript)
        
        try:
            # Call the LLM based on the selected model
            response = self._call_llm(formatted_prompt)
            print(f"LLM response: {response}")
            return response
        except Exception as e:
            raise Exception(f"LLM processing error: {str(e)}")
    
    def _call_llm(self, prompt):
        """Call the LLM using litellm"""
        try:
            if self.model == "OPENAI":
                response = completion(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}]
                )
            elif self.model == "ANTHROPIC":
                response = completion(
                    model="anthropic/claude-3-7-sonnet-20250219",
                    messages=[{"role": "user", "content": prompt}]
                )
            else:  # GEMINI with API token only (no Vertex, no google.auth)
                response = completion(
                    model="gemini/gemini-2.0-flash",
                    messages=[{"role": "user", "content": prompt}],
                )
            
            # Extract and return the content
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"LLM API error: {str(e)}")