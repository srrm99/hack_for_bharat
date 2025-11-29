# Project Structure

## 📁 Bharat Context-Adaptive Engine

```
Bharat/
├── signals.md                    # Exhaustive list of implicit signals taxonomy
├── rules.yaml                    # Inference rules and scoring configuration
├── models.py                     # Pydantic models for signals and inference output
├── inference_engine.py           # Core inference engine logic
├── router_inference.py           # FastAPI router with /v1/infer endpoint
├── main.py                       # FastAPI application entry point
├── test_inference_engine.py      # Unit tests for inference engine
├── test_api.py                   # API integration tests
├── requirements.txt              # Python dependencies
├── example_payloads.json         # Example API request payloads
├── README.md                     # Full documentation
├── QUICKSTART.md                 # Quick start guide
├── PROJECT_STRUCTURE.md          # This file
└── .gitignore                    # Git ignore rules
```

## 📋 File Descriptions

### Core Files

1. **signals.md**
   - Complete taxonomy of 100+ implicit signals
   - Organized into 12 categories (Device, Network, Locale, Time, etc.)
   - Privacy-first signal collection principles
   - Signal priority levels

2. **rules.yaml**
   - 11+ inference rules for different user need states
   - Weighted scoring system
   - Confidence thresholds
   - Recommended actions per rule
   - Extensible rule engine configuration

3. **models.py**
   - Pydantic models for type safety
   - `RawSignals`: Input signal model
   - `InferenceOutput`: Output model
   - `InferenceRequest/Response`: API models
   - Enums for signal values

4. **inference_engine.py**
   - `InferenceEngine`: Main engine class
   - `extract_signals()`: Signal extraction and validation
   - `score_rules()`: Rule scoring against signals
   - `infer_need_state()`: User need state inference
   - `generate_recommendations()`: Action recommendations
   - `generate_explanation()`: Human-readable explanations

5. **router_inference.py**
   - `/v1/infer`: Main inference endpoint
   - `/v1/health`: Health check endpoint
   - `/v1/rules`: Rules listing endpoint
   - `/v1/infer/batch`: Batch inference endpoint

6. **main.py**
   - FastAPI application setup
   - CORS middleware configuration
   - Router registration
   - Global exception handling

### Test Files

7. **test_inference_engine.py**
   - Unit tests for inference engine
   - Rule condition evaluation tests
   - Edge case handling tests

8. **test_api.py**
   - API endpoint integration tests
   - Request/response validation tests
   - Error handling tests

### Documentation

9. **README.md**
   - Complete project documentation
   - Installation instructions
   - API usage examples
   - Configuration guide
   - Troubleshooting

10. **QUICKSTART.md**
    - 5-minute quick start guide
    - Common use cases
    - Example payloads

11. **example_payloads.json**
    - 11 example request payloads
    - Different user scenarios
    - Expected responses

### Configuration

12. **requirements.txt**
    - Python dependencies
    - FastAPI, Pydantic, PyYAML
    - Testing libraries

13. **.gitignore**
    - Python cache files
    - Virtual environments
    - IDE files
    - Logs and databases

## 🏗️ Architecture Flow

```
Client App
    ↓
Raw Signals (JSON)
    ↓
FastAPI /v1/infer
    ↓
InferenceEngine.extract_signals()
    ↓
InferenceEngine.score_rules()
    ↓
InferenceEngine.infer_need_state()
    ↓
InferenceEngine.generate_recommendations()
    ↓
InferenceOutput (JSON)
    ↓
Client App (UI Adaptation)
```

## 🔄 Data Flow

1. **Input**: Raw signals from client app (device, network, time, locale, etc.)
2. **Processing**: 
   - Signal extraction and validation
   - Rule scoring (weighted sum)
   - Need state inference
   - Recommendation generation
3. **Output**: User need state, confidence, actions, UI mode, language preference

## 🎯 Key Features

✅ **Modular Design**: Easy to extend with new rules and signals
✅ **YAML-based Rules**: No code changes needed to modify rules
✅ **Type Safety**: Pydantic models for validation
✅ **Test Coverage**: Unit and integration tests
✅ **Documentation**: Comprehensive docs and examples
✅ **Privacy-First**: Coarse-grained, non-identifying signals
✅ **Extensible**: Ready for ML-based scoring upgrade

## 🚀 Next Steps for Extension

1. **Add ML Models**: Replace rule scoring with ML inference
2. **Add Caching**: Cache frequent inference results
3. **Add Monitoring**: Metrics and logging
4. **Add Authentication**: API key or OAuth
5. **Add Rate Limiting**: Prevent abuse
6. **Add Database**: Store inference history (anonymized)

