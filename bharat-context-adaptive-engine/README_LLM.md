# Bharat Context-Adaptive Engine

## Overview
This engine infers user "Need States" from implicit mobile signals (location, apps, usage patterns) specifically for the Indian (Bharat) context. It uses a hybrid approach:
1.  **Rule-based Inference**: Deterministic rules for common patterns.
2.  **LLM Reasoning (OpenRouter)**: Uses GPT-5.1 with reasoning to infer complex user profiles.
3.  **Web Intelligence (Perplexity)**: Fetches real-time context about digital trends in India.

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Environment Variables**:
    Create a `.env` file or export these variables:
    ```bash
    export OPENROUTER_API_KEY="your_openrouter_key"
    export PERPLEXITY_API_KEY="your_perplexity_key"
    ```

3.  **Run the Server**:
    ```bash
    cd src
    uvicorn main:app --reload
    ```

## Architecture

-   **Signal Data**: Collected from device (see `src/models.py` for schema).
-   **Inference Engine**: `src/inference_engine_enhanced.py` orchestrates the process.
-   **LLM Service**: `src/llm_service.py` handles OpenRouter and Perplexity calls.
-   **Recommendations**: `src/recommendation_engine.py` maps Need States to content (Day 0/1/7).

## Testing

Run the integration test to verify the LLM flow (uses mocks):
```bash
python3 -m unittest tests/test_integration_llm.py
```

