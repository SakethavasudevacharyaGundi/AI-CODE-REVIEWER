import json 
from pathlib import Path
import requests

BASE_URL = "http://127.0.0.1:8000"
DIFFS = [
    {
        "input": "diff/diff1_python.txt",
        "output": "reviews/diff1_review.json",
        "language": "python",
        "context": "Diff 1 review"
    },
    {
        "input": "diff/diff2_javascript.txt",
        "output": "reviews/diff2_review.json",
        "language": "javascript",
        "context": "Diff 2 review"
    },
    {
        "input": "diff/diff3_typescript.txt",
        "output": "reviews/diff3_review.json",
        "language": "typescript",
        "context": "Diff 3 review"
    }
]
def review_diff(diff_file:str,output_file:str,language:str,context:str):
    diff_path=Path(diff_file)
    if not diff_path.exists():
        raise FileNotFoundError(f"Diff file {diff_file} not found")
    print("Reviewing diff:",diff_file)
    diff_text=diff_path.read_text(encoding="utf-8")
    payload={
        "diff":diff_text,
        "language":language,
        "context":context
    }
    response=requests.post(
        f"{BASE_URL}/review",
        json=payload,
        timeout=300
    )
    print("Response status code:",response.status_code)
    if response.status_code!=200:
        print("Error response:")
        print(response.text[:5000])
        return
    try:
        review=response.json()
    except Exception:
        print("Failed to parse JSON response:")
        print(response.text[:5000])
        return
    output_path=Path(output_file)
    output_path.parent.mkdir(parents=True,exist_ok=True)

    with open(output_file,"w",encoding="utf-8") as f:
        json.dump(review,f,indent=2)

    print(f"Saved review to {output_file}")
def main():
    print("Generating reviews:")
    for diff in DIFFS:
        review_diff(diff["input"], diff["output"], diff["language"], diff["context"])
    print("All reviews generated successfully")
if __name__ == "__main__":
    main()