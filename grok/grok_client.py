#!/usr/bin/env python3
"""
Grok Client for Resonant Vortex Reactor Project
xAI Grok API integration with query and batch support.
"""

import os
import json
import requests
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

class GrokClient:
    def __init__(self):
        self.api_key = os.getenv("GROK_API_KEY")
        if not self.api_key:
            raise ValueError("GROK_API_KEY not found in environment variables.")
        
        self.base_url = "https://api.grok.x.ai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def query(self, prompt: str, model: str = "grok-beta", temperature: float = 0.7, max_tokens: int = 2048) -> str:
        """Single query to Grok."""
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        response = requests.post(self.base_url, headers=self.headers, json=payload)
        response.raise_for_status()
        
        return response.json()["choices"][0]["message"]["content"]

    def batch_query(self, prompts: List[str], model: str = "grok-beta", temperature: float = 0.7) -> List[str]:
        """Batch multiple queries."""
        results = []
        for prompt in prompts:
            try:
                result = self.query(prompt, model, temperature)
                results.append(result)
            except Exception as e:
                results.append(f"Error: {str(e)}")
        return results

    def analyze_simulation(self, csv_path: str) -> str:
        """Example: Analyze simulation CSV data."""
        prompt = f"Analyze the following simulation data from {csv_path} and summarize key patterns, peaks, and insights for the Gali-Spinal Tube project."
        # In production, read the CSV and include data in prompt
        return self.query(prompt)

if __name__ == "__main__":
    client = GrokClient()
    
    # Example usage
    response = client.query("Summarize the current state of the Resonant Vortex Reactor project.")
    print(response)