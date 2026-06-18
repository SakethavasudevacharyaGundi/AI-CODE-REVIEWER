from typing import Literal
from pydantic import BaseModel
from app.models.finding import Finding

class ReviewReport(BaseModel):
    pr_summary:str
    verdict :Literal["approve", "request_changes", "needs_discussion"]
    verdict_reason:str
    overall_severity:Literal["low", "medium", "high","critical","clean"]
    findings:list[Finding]
    positive_observations:list[str]
    missing_tests:list[str]
    agent_findings_count:dict[str,int]
    processing_time_ms:int