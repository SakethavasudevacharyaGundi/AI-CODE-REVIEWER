from app.graph.state import ReviewState
from app.models.review_report import ReviewReport
from app.reviewers.security import analyze_security
from app.reviewers.style import analyze_style
from app.reviewers.test_coverage import analyze_test_coverage
from app.reviewers.correctness import analyze_correctness
from app.reviewers.performance import analyze_performance
from app.reviewers.report_generator import generate_report_sections
from app.utils.diff_parser import assign_line_numbers
import time

def security_reviewer(state:ReviewState):
    findings=analyze_security(state["diff"])
    return  {"security_findings":findings}
def performance_reviewer(state:ReviewState):
    findings=analyze_performance(state["diff"])
    return  {"performance_findings":findings}
def correctness_reviewer(state:ReviewState):
    findings=analyze_correctness(state["diff"])
    return  {"correctness_findings":findings}
def style_reviewer(state:ReviewState):
    findings=analyze_style(state["diff"])
    return  {"style_findings":findings}
def test_coverage_reviewer(state:ReviewState):
    findings=analyze_test_coverage(state["diff"])
    return  {"test_coverage_findings":findings}
def calculate_overall_severity(findings:list):
    if any(f.severity=="critical" for f in findings):
        return "critical"
    if any(f.severity=="high" for f in findings):
        return "high"
    if any(f.severity=="medium" for f in findings):
        return "medium"
    if any(f.severity=="low" for f in findings):
        return "low"
    return "clean"
def generate_verdict(severity):
    if severity in ["critical", "high"]:
        return "request_changes"
    if severity in ["medium","low"]:
        return "needs_discussion"
    return "approve"
def merge_node(state:ReviewState):
    all_findings = (
    state["security_findings"]
    + state["performance_findings"]
    + state["correctness_findings"]
    + state["style_findings"]
    )
    seen=set()
    deduped_findings=[]
    for finding in all_findings:
        key=(finding.category,finding.title.lower().strip(),finding.line_content.strip()[:100])
        if key not in seen:
            seen.add(key)
            deduped_findings.append(finding)
    all_findings = deduped_findings
    all_findings=assign_line_numbers(state["diff"],all_findings)
    processing_time_ms=int((time.time() - state["start_time"])*1000)
    for i,finding in enumerate(all_findings,start=1):
        finding.id = f"F-{i:03d}"
    overall_severity = calculate_overall_severity(all_findings)
    verdict = generate_verdict(overall_severity)
    report_sections=generate_report_sections(
            diff=state["diff"],
            findings=all_findings,
            overall_severity=overall_severity,
            verdict=verdict
    )  
    report=ReviewReport(
        pr_summary=report_sections.pr_summary,
        verdict_reason=report_sections.verdict_reason,
        overall_severity=overall_severity,
        verdict=verdict,
        findings=all_findings,
        positive_observations=report_sections.positive_observations,
        missing_tests=state["test_coverage_findings"],
        agent_findings_count={
            "security": len(state["security_findings"]),
            "performance": len(state["performance_findings"]),
            "correctness": len(state["correctness_findings"]),
            "style": len(state["style_findings"]),
            "test_coverage": len(state["test_coverage_findings"]),
        },
        processing_time_ms=processing_time_ms
    )
    return {"review_report":report}