from fastapi import FastAPI,HTTPException
from app.models.review_request import ReviewRequest
from app.graph.builder import graph
from app.storage.reviews import save_review, get_review, list_reviews
from app.llm import get_llm
import time
import uuid
app = FastAPI()
llm = get_llm()
@app.get("/")
def root():
    return {"message": "AI Code Reviewer API"}
@app.post("/review")
def review_code(request: ReviewRequest):
    result=graph.invoke({
        "diff":request.diff,
        "start_time":time.time(),
        "language":request.language,
        "context":request.context,
        "security_findings":[],
        "performance_findings":[],
        "correctness_findings":[],
        "style_findings":[],
        "test_coverage_findings":[],
    }
    )
    report =result["review_report"]
    review_id=str(uuid.uuid4())
    save_review(review_id, report)
    return report
@app.get("/review/{review_id}")
def get_review_by_id(review_id:str):
    review=get_review(review_id)
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return review["review"]
@app.get("/reviews")
def get_all_reviews():
    response=[]
    for review_id,data in list_reviews().items():
        report=data["review"]
        response.append({
            "review_id":review_id,
            "pr_summary":report.pr_summary,
            "verdict":report.verdict,
            "overall_severity":report.overall_severity,
            "created_at":data["created_at"],
        })
    return response
@app.get("/health")
def health():
    try:
        llm.invoke("ping")
        return{
            "status":"healthy",
            "gorq_status":"healthy"
        }
    except Exception as e:
        return{
            "status":"unhealthy",
            "gorq_status":"unhealthy",
            "error":str(e)
        }