"""
FastAPI router for recommendation endpoints
"""

from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, status, Query
from .models import InferenceRequest, InferenceOutput
from .inference_engine_enhanced import get_enhanced_inference_engine
from .recommendation_engine import RecommendationEngine

router = APIRouter(prefix="/v1/recommendations", tags=["recommendations"])

recommendation_engine = RecommendationEngine()


@router.post("/generate")
async def generate_recommendations(
    request: InferenceRequest,
    day: int = Query(0, description="Day number (0=Day-0, 1=Day-1, 7=Day-7)"),
    enhanced: bool = Query(True, description="Use enhanced inference engine")
) -> Dict[str, Any]:
    """
    Generate personalized recommendations based on signals
    
    Flow:
    1. Run inference engine to get user need state
    2. Generate recommendations based on day (0, 1, 7)
    3. Return content, delivery medium, and timing
    
    Args:
        request: InferenceRequest with signals
        day: Day number (0 = Day-0, 1 = Day-1, 7 = Day-7)
        enhanced: Use enhanced inference engine
        
    Returns:
        Dictionary with inference output and recommendations
    """
    try:
        # Step 1: Run inference engine
        if enhanced:
            engine = get_enhanced_inference_engine()
        else:
            from .inference_engine import get_inference_engine
            engine = get_inference_engine()
        
        inference_output = engine.infer(request.signals)
        
        # Step 2: Generate recommendations
        recommendations = recommendation_engine.generate_recommendations(
            inference_output=inference_output,
            day=day
        )
        
        return {
            "success": True,
            "inference": {
                "user_need_state": inference_output.user_need_state,
                "confidence": inference_output.confidence,
                "ui_mode": inference_output.ui_mode.value,
                "language_preference": inference_output.language_preference.value
            },
            "recommendations": recommendations,
            "day": day
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating recommendations: {str(e)}"
        )


@router.post("/all-days")
async def generate_all_days_recommendations(
    request: InferenceRequest,
    enhanced: bool = Query(True, description="Use enhanced inference engine")
) -> Dict[str, Any]:
    """
    Generate recommendations for Day-0, Day-1, and Day-7
    
    Returns complete recommendation strategy for all days
    """
    try:
        # Run inference
        if enhanced:
            engine = get_enhanced_inference_engine()
        else:
            from .inference_engine import get_inference_engine
            engine = get_inference_engine()
        
        inference_output = engine.infer(request.signals)
        
        # Generate for all days
        day_0 = recommendation_engine.generate_recommendations(inference_output, day=0)
        day_1 = recommendation_engine.generate_recommendations(inference_output, day=1)
        day_7 = recommendation_engine.generate_recommendations(inference_output, day=7)
        
        return {
            "success": True,
            "inference": {
                "user_need_state": inference_output.user_need_state,
                "confidence": inference_output.confidence,
                "ui_mode": inference_output.ui_mode.value,
                "language_preference": inference_output.language_preference.value
            },
            "recommendations": {
                "day_0": day_0,
                "day_1": day_1,
                "day_7": day_7
            }
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating recommendations: {str(e)}"
        )

