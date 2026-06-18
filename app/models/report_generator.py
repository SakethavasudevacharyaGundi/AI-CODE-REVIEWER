from pydantic import BaseModel
class ReportGeneratorInput(BaseModel):
    pr_summary:str
    verdict_reason:str
    positive_observations:list[str]