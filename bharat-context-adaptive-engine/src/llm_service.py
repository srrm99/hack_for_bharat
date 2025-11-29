"""
LLM Service for Bharat Context-Adaptive Engine
Handles interactions with OpenRouter (Reasoning Models) and Perplexity (Web Intelligence)
"""

import os
import json
import httpx
from typing import Dict, Any, List, Optional
from datetime import datetime, date
from openai import OpenAI
from dotenv import load_dotenv
from .models import RawSignals, InferenceOutput, UIMode, LanguagePreference

# Load environment variables from .env file
load_dotenv()

class LLMService:
    def __init__(self):
        self.openrouter_key = os.getenv("OPENROUTER_API_KEY")
        self.perplexity_key = os.getenv("PERPLEXITY_API_KEY")
        
        # Initialize OpenRouter client if key exists
        if self.openrouter_key:
            self.openai_client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=self.openrouter_key,
            )
        else:
            self.openai_client = None

        # Perplexity client configuration
        self.perplexity_url = "https://api.perplexity.ai/chat/completions"

    def get_web_intelligence(self, query: str) -> str:
        """
        Get real-time web intelligence using Perplexity Sonar API
        """
        if not self.perplexity_key:
            print("Warning: PERPLEXITY_API_KEY not set. Returning mock response.")
            return "Web intelligence unavailable (API Key missing)."

        headers = {
            "Authorization": f"Bearer {self.perplexity_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "sonar-pro",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful research assistant focusing on Indian SMB and consumer trends."
                },
                {
                    "role": "user",
                    "content": query
                }
            ]
        }

        try:
            # Use httpx for synchronous request (can be asyncified if needed)
            response = httpx.post(self.perplexity_url, json=payload, headers=headers, timeout=30.0)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Perplexity API Error: {e}")
            return f"Error fetching web intelligence: {str(e)}"

    def infer_user_profile_with_reasoning(self, signals: RawSignals, rules_context: str = "") -> Dict[str, Any]:
        """
        Use OpenRouter with reasoning to infer user profile from signals
        """
        if not self.openai_client:
            return {
                "error": "OpenRouter API Key not configured",
                "user_need_state": "Default User",
                "confidence": 0.0
            }

        # Helper for JSON serialization
        def json_serial(obj):
            if isinstance(obj, (datetime, date)):
                return obj.isoformat()
            return str(obj)

        # Convert signals to a clean JSON string
        signals_dict = signals.model_dump(exclude_none=True)
        signals_json = json.dumps(signals_dict, indent=2, default=json_serial)

        system_prompt = f"""
You are an advanced AI Inference Engine for the 'Bharat Context-Adaptive Engine'.
Your goal is to analyze raw mobile device signals and infer the 'User Need State' for an Indian user (SMB owner, student, etc.).

CONTEXT FROM RULES (Use as guidance):
{rules_context}

TASK:
1. Analyze the provided Signal Data.
2. Use reasoning to determine the most likely User Persona and Need State.
3. Consider the Indian context (Tier-2/3 cities, cultural nuances).
4. Output a JSON object with:
   - user_need_state: (string) e.g., "Evening Ledger / Khatabook Mode User"
   - confidence: (float 0-10)
   - reasoning_summary: (string) Brief explanation
   - recommended_actions: (list of strings) 3-5 UI actions
   - ui_mode: (string) "standard", "lite", or "voice-first"
   - language_preference: (string) "hindi", "english", "regional", etc.
"""

        user_message = f"""
Here is the Signal Data for a user:
{signals_json}

Analyze this user and provide the inference.
"""

        try:
            # First API call with reasoning enabled
            response = self.openai_client.chat.completions.create(
                model="openai/gpt-5.1",  # As requested by user
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                extra_body={"reasoning": {"enabled": True}},
                response_format={"type": "json_object"} 
            )
            
            content = response.choices[0].message.content
            try:
                result = json.loads(content)
                return result
            except json.JSONDecodeError:
                return {"error": "Failed to parse JSON response", "raw_content": content}

        except Exception as e:
            print(f"OpenRouter API Error: {e}")
            return {"error": str(e)}

    def generate_feed_from_perplexity(self, user_need_state: str, language: str) -> List[Dict[str, Any]]:
        """
        Generate personalized feed items using Perplexity Sonar API
        """
        if not self.perplexity_key:
            return []

        query = f"""
        Generate 3 specific, high-relevance news headlines or actionable tips for a user who is identified as '{user_need_state}' in India. 
        Focus on recent updates (finance, education, business, or local news depending on the persona).
        Return ONLY a JSON list of objects with these keys: 'id' (unique string), 'type' (news/insight), 'title', 'summary', 'source', 'time', 'tags' (list of strings).
        """

        headers = {
            "Authorization": f"Bearer {self.perplexity_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "sonar-pro",
            "messages": [
                {"role": "system", "content": "You are a content recommendation engine for Indian users. Output valid JSON only."},
                {"role": "user", "content": query}
            ]
        }

        try:
            response = httpx.post(self.perplexity_url, json=payload, headers=headers, timeout=30.0)
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
            
            # Clean up markdown code blocks if present
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
                
            return json.loads(content)
        except Exception as e:
            print(f"Perplexity Feed Gen Error: {e}")
            return []

    def chat_completion(self, messages: List[Dict[str, str]], context: str = "") -> str:
        """
        Chat with context using OpenRouter
        """
        if not self.openai_client:
            return "Chat service unavailable (API Key missing)."

        system_prompt = f"""You are BharatAI, a helpful assistant for Indian users.
Context regarding the current topic:
{context}

Answer the user's question helpfully and concisely."""

        # Prepend system message
        full_messages = [{"role": "system", "content": system_prompt}] + messages

        try:
            response = self.openai_client.chat.completions.create(
                model="openai/gpt-5.1", # or use a cheaper/faster model for chat like gpt-4o-mini or llama-3
                messages=full_messages
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Chat Completion Error: {e}")
            return f"Sorry, I encountered an error: {str(e)}"

# Singleton instance
_llm_service = None

def get_llm_service():
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service

