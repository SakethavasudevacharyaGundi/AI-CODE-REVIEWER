from pydantic import BaseModel
from app.models.finding import Finding
from app.llm import get_llm
    
llm = get_llm()

class StyleReviewOutput(BaseModel):
    findings: list[Finding]

with open(
    "app/prompts/style_prompt.txt",
    "r",
    encoding="utf-8"
) as f:
    STYLE_PROMPT = f.read()

structured_llm = llm.with_structured_output(
    StyleReviewOutput
)

def analyze_style(diff: str):
    response = structured_llm.invoke(
        f"""
{STYLE_PROMPT}

Review this diff:

{diff}
"""
    )

    return response.findings