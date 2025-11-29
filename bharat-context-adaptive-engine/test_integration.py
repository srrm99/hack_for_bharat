import unittest
from unittest.mock import MagicMock, patch
import json
from datetime import datetime

from src.models import RawSignals, InferenceOutput
from src.inference_engine_enhanced import EnhancedInferenceEngine
from src.llm_service import LLMService

class TestBharatEngine(unittest.TestCase):
    def setUp(self):
        self.mock_signals = RawSignals(
            device_class="low_end",
            network_type="2g",
            business_apps=["khatabook"],
            whatsapp_business_usage="yes",
            time_of_day="evening",
            system_language="hi"
        )

    @patch('src.llm_service.OpenAI')
    @patch('src.llm_service.httpx.post')
    def test_full_flow(self, mock_httpx, mock_openai):
        # Mock Perplexity response
        mock_httpx.return_value.json.return_value = {
            "choices": [{"message": {"content": "SMBs in India use WhatsApp for business."}}]
        }
        mock_httpx.return_value.raise_for_status = MagicMock()

        # Mock OpenRouter response
        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = json.dumps({
            "user_need_state": "Evening Ledger / Khatabook Mode User",
            "confidence": 9.5,
            "reasoning_summary": "User has business apps and is active in evening.",
            "recommended_actions": ["GST Calc", "Invoice", "Profit Calc"],
            "ui_mode": "standard",
            "language_preference": "hindi"
        })
        mock_openai.return_value.chat.completions.create.return_value = mock_completion

        # Initialize engine
        engine = EnhancedInferenceEngine()
        
        # Mock the LLMService instance inside the engine components
        engine.llm_reasoning.llm_service.openai_client = mock_openai.return_value
        engine.llm_reasoning.llm_service.perplexity_key = "mock_key"
        engine.web_intelligence.llm_service.perplexity_key = "mock_key"

        # Run inference
        result = engine.infer(self.mock_signals)

        # Assertions
        self.assertIsInstance(result, InferenceOutput)
        self.assertEqual(result.user_need_state, "Evening Ledger / Khatabook Mode User")
        self.assertGreater(result.confidence, 8.0)
        self.assertEqual(result.language_preference, "hindi")
        
        print(f"\nInference Result: {result.user_need_state} (Confidence: {result.confidence})")
        print(f"Explanation: {result.explanation[:100]}...")

if __name__ == '__main__':
    unittest.main()

