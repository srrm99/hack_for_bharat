"""
FastAPI router for inference endpoints
"""

import time
from typing import Dict, Any, Optional, List
from fastapi import APIRouter, HTTPException, status, Query, Body
from fastapi.responses import JSONResponse

from .models import InferenceRequest, InferenceResponse, HealthCheck
from .inference_engine import get_inference_engine, InferenceEngine
from .inference_engine_enhanced import get_enhanced_inference_engine, EnhancedInferenceEngine
from .explanation_models import InferenceExplanation


router = APIRouter(prefix="/v1", tags=["inference"])


@router.post("/chat")
async def chat_with_context(
    messages: List[Dict[str, str]] = Body(..., description="Chat history"),
    context: str = Body("", description="Context for the chat")
) -> Dict[str, Any]:
    """
    Chat with the AI assistant using specific context
    """
    try:
        service = get_llm_service()
        response = service.chat_completion(messages, context)
        return {
            "success": True,
            "response": response
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@router.post("/chat")
async def chat_with_context(
    messages: List[Dict[str, str]] = Body(..., description="Chat history"),
    context: str = Body("", description="Context for the chat")
) -> Dict[str, Any]:
    """
    Chat with the AI assistant using specific context
    """
    try:
        service = get_llm_service()
        response = service.chat_completion(messages, context)
        return {
            "success": True,
            "response": response
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@router.post("/chat")
async def chat_with_context(
    messages: List[Dict[str, str]] = Body(..., description="Chat history"),
    context: str = Body("", description="Context for the chat")
) -> Dict[str, Any]:
    """
    Chat with the AI assistant using specific context
    """
    try:
        service = get_llm_service()
        response = service.chat_completion(messages, context)
        return {
            "success": True,
            "response": response
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@router.post("/infer", response_model=InferenceResponse)
async def infer_user_need_state(
    request: InferenceRequest, 
    enhanced: bool = Query(True, description="Use enhanced inference engine with web intelligence, app context, and LLM reasoning")
) -> InferenceResponse:
    """
    Infer user need state from implicit signals
    
    This endpoint takes raw signals from the client app and returns:
    - User need state (e.g., "Morning Devotional User", "Student Exam Time User")
    - Confidence score (0-10)
    - Recommended actions (3-5 items)
    - UI mode (standard/lite/voice-first)
    - Language preference
    - Explanation of inference
    
    Uses enhanced inference engine with:
    - Web intelligence (signal pattern knowledge)
    - App context (ChatGPT-specific understanding)
    - LLM reasoning (worldly knowledge and correlations)
    - Detailed explanation logging
    
    Args:
        request: InferenceRequest containing raw signals
        enhanced: Use enhanced inference engine (default: True)
        
    Returns:
        InferenceResponse with inference results
    """
    start_time = time.time()
    
    try:
        # Get enhanced inference engine instance
        if enhanced:
            engine = get_enhanced_inference_engine()
        else:
            engine = get_inference_engine()
        
        # Extract signals from request
        signals = request.signals
        
        # Run inference
        inference_output = engine.infer(signals)
        
        # Get inference ID if enhanced engine
        inference_id = None
        if enhanced and hasattr(engine, 'explanations'):
            # Find the most recent explanation
            if engine.explanations:
                inference_id = max(engine.explanations.keys(), 
                                 key=lambda k: engine.explanations[k].timestamp)
        
        # Calculate processing time
        processing_time_ms = (time.time() - start_time) * 1000
        
        # Add inference ID to explanation if available
        if inference_id:
            inference_output.explanation += f"\n\n[Inference ID: {inference_id}]"
        
        return InferenceResponse(
            success=True,
            data=inference_output,
            error=None,
            processing_time_ms=processing_time_ms
        )
    
    except Exception as e:
        processing_time_ms = (time.time() - start_time) * 1000
        
        return InferenceResponse(
            success=False,
            data=None,
            error=str(e),
            processing_time_ms=processing_time_ms
        )


@router.get("/health", response_model=HealthCheck)
async def health_check() -> HealthCheck:
    """
    Health check endpoint
    
    Returns service status and configuration info
    """
    try:
        engine = get_inference_engine()
        
        return HealthCheck(
            status="healthy",
            version="1.0.0",
            rules_loaded=True,
            rules_count=len(engine.rules)
        )
    
    except Exception as e:
        return HealthCheck(
            status="unhealthy",
            version="1.0.0",
            rules_loaded=False,
            rules_count=0
        )


@router.get("/rules")
async def list_rules() -> Dict[str, Any]:
    """
    List all available inference rules
    
    Returns metadata about all loaded rules
    """
    try:
        engine = get_inference_engine()
        
        rules_info = []
        for rule in engine.rules:
            rules_info.append({
                "name": rule.name,
                "description": rule.description,
                "confidence_threshold": rule.confidence_threshold,
                "condition_count": len(rule.conditions)
            })
        
        return {
            "total_rules": len(engine.rules),
            "rules": rules_info,
            "scoring_method": engine.scoring_config.get("method", "weighted_sum"),
            "default_rule": engine.default_rule.get("user_need_state", "Unknown")
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error loading rules: {str(e)}"
        )


@router.get("/infer/explanation/{inference_id}")
async def get_inference_explanation(inference_id: str) -> Dict[str, Any]:
    """
    Get detailed explanation for an inference
    
    Returns complete explanation including:
    - Signal analysis
    - Web intelligence insights
    - App context insights
    - LLM reasoning steps
    - Rule scoring details
    - Decision factors
    """
    try:
        engine = get_enhanced_inference_engine()
        explanation = engine.get_explanation(inference_id)
        
        if not explanation:
            return {
                "success": False,
                "error": f"Explanation not found for inference ID: {inference_id}"
            }
        
        return {
            "success": True,
            "inference_id": inference_id,
            "explanation": explanation.dict(),
            "human_readable": explanation.generate_human_readable()
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@router.post("/infer/log/{inference_id}")
async def log_inference_explanation(inference_id: str, file_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Log inference explanation to file
    
    Args:
        inference_id: Inference ID to log
        file_path: Optional custom file path (default: explanations/{inference_id}.log)
    """
    try:
        engine = get_enhanced_inference_engine()
        engine.log_explanation(inference_id, file_path)
        
        return {
            "success": True,
            "message": f"Explanation logged for inference ID: {inference_id}",
            "file_path": file_path or f"explanations/{inference_id}.log"
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@router.post("/infer/batch")
async def infer_batch(requests: list[InferenceRequest]) -> Dict[str, Any]:
    """
    Batch inference endpoint for multiple signals
    
    Processes multiple inference requests in a single call
    """
    start_time = time.time()
    results = []
    
    try:
        engine = get_inference_engine()
        
        for request in requests:
            try:
                inference_output = engine.infer(request.signals)
                results.append({
                    "success": True,
                    "data": inference_output.dict(),
                    "error": None
                })
            except Exception as e:
                results.append({
                    "success": False,
                    "data": None,
                    "error": str(e)
                })
        
        processing_time_ms = (time.time() - start_time) * 1000
        
        return {
            "success": True,
            "results": results,
            "total_processed": len(requests),
            "processing_time_ms": processing_time_ms
        }
    
    except Exception as e:
        return {
            "success": False,
            "results": [],
            "total_processed": 0,
            "error": str(e),
            "processing_time_ms": (time.time() - start_time) * 1000
        }

