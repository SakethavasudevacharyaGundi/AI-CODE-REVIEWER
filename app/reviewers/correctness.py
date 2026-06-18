from pydantic import BaseModel
from app.models.finding import Finding
from app.llm import get_llm

class CorrectnessReviewOutput(BaseModel):
    findings: list[Finding]

with open(
    "app/prompts/correctness_prompt.txt",
    "r",
    encoding="utf-8"
) as f:
    CORRECTNESS_PROMPT = f.read()
llm = get_llm()
structured_llm = llm.with_structured_output(
    CorrectnessReviewOutput
)

def analyze_correctness(diff: str):
    response = structured_llm.invoke(
        f"""
{CORRECTNESS_PROMPT}

Review this diff:

{diff}
"""
    )

    return response.findings