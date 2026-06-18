from app.llm import get_llm
from app.models.report_generator import ReportGeneratorInput
with open("app/prompts/report_generator_prompt.txt", "r", encoding="utf-8") as f:
    ReportGeneratorPrompt = f.read()
structured_llm = get_llm().with_structured_output(ReportGeneratorInput)
def generate_report_sections(
        diff:str,
        findings,
        overall_severity:str,
        verdict:str,
):
    response = structured_llm.invoke(f"""{ReportGeneratorPrompt}diff:{diff} Findings:{findings} OverallSeverity:{overall_severity} Verdict:{verdict}""")
    return response 