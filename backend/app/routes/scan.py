from fastapi import APIRouter
from app.models.schema import Policy
from app.core.scanner import scan_iam_policy
from app.services.ai_explainer import explain_all_threats 

router = APIRouter()

@router.post("/scan")
def scan_policy_endpoint(payload: Policy):
    # 1. Run the core logic to identify security rules violated
    threats, score = scan_iam_policy(payload.policy)
    
    # 2. Call the Batch AI function to get explanations for all threats at once
    # This prevents the '429 Rate Limit' and '404 Not Found' errors
    if threats:
        enriched_threats = explain_all_threats(threats)
    else:
        enriched_threats = []

    # 3. Return the data structure the React dashboard needs to populate the table
    return {
        "score": score,
        "threats": enriched_threats
    }