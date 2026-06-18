from typing import TypedDict
from app.models.review_report import ReviewReport
from app.models.finding import Finding
class ReviewState(TypedDict):
    diff:str
    language:str
    context:str|None
    security_findings:list[Finding]
    performance_findings:list[Finding]
    correctness_findings:list[Finding]
    style_findings:list[Finding]
    test_coverage_findings:list[Finding]
    start_time:float
    review_report:ReviewReport
