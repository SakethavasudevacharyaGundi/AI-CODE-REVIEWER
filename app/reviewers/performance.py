from pydantic import BaseModel
from app.models.finding import Finding
from app.llm import get_llm

class PerformanceReviewOutput(BaseModel):
    findings: list[Finding]
with open("app/prompts/performance_prompt.txt", "r", encoding="utf-8") as f:
    PERFORMANCE_PROMPT = f.read()
llm=get_llm()
structured_llm = llm.with_structured_output(PerformanceReviewOutput)

def analyze_performance(diff: str):
    response = structured_llm.invoke(f"""{PERFORMANCE_PROMPT}Review this diff:{diff}""")
    return response.findings