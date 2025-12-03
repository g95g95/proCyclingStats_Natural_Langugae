"""Chat API endpoints."""

from fastapi import APIRouter, Depends, HTTPException

from app.models.chat import ChatRequest, ChatResponse
from app.services.ai_service import AIService
from app.services.pcs_scraper import PCSScraperService
from app.dependencies import get_scraper

router = APIRouter()


@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    scraper: PCSScraperService = Depends(get_scraper)
):
    """
    Process a chat message and return AI response with optional data.
    """
    try:
        ai_service = AIService(scraper)
        response = await ai_service.chat(request.message)

        return ChatResponse(
            message=response["message"],
            data=response.get("data"),
            visualization=response.get("visualization")
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/quick")
async def quick_query(
    query: str,
    scraper: PCSScraperService = Depends(get_scraper)
):
    """
    Quick query endpoint for simple questions.
    Returns structured data without full AI processing.
    """
    try:
        ai_service = AIService(scraper)
        plan = await ai_service.plan_query(query)
        data = await ai_service.execute_query(plan)

        return {
            "plan": plan,
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
