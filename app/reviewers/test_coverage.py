from pydantic import BaseModel
from app.llm import get_llm
llm=get_llm()

class TestCoverageReviewOutput(BaseModel):
    missing_tests:list[str]

with open("app/prompts/test_coverage_prompt.txt", "r", encoding="utf-8") as f:
    TestCoveragePrompt = f.read()
structured_llm = llm.with_structured_output(TestCoverageReviewOutput)

def analyze_test_coverage(diff:str) -> TestCoverageReviewOutput:
    response = structured_llm.invoke(f"""{TestCoveragePrompt}Review this diff:{diff}""")
    return response.missing_tests
