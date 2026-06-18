from pathlib import Path
from pydantic import BaseModel
from app.llm import get_llm
from app.models.finding import Finding

class SecurityReviewOutput(BaseModel):
    findings:list[Finding]

def analyze_security(diff:str)->list[Finding]:
    prompt = Path("app/prompts/security_prompt.txt").read_text(encoding="utf-8")
    llm=get_llm()
    structured_llm=llm.with_structured_output(SecurityReviewOutput)
    result=structured_llm.invoke(f"{prompt}\n\nGit diff:\n{diff}")
    return result.findings