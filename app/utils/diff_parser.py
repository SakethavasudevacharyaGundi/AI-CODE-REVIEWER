def build_line_map(diff:str)->dict[str,int]:
    line_map={}
    current_line=0
    for line in diff.splitlines():
        if line.startswith("@@"):
            try:
                new_file_info=line.split("+")[1].split(" ")[0]
                current_line=int(new_file_info.split(",")[0])-1
            except Exception:
                continue
            continue
        if line.startswith("+++"):
            continue
        if line.startswith("+"):
            current_line+=1
            content=line[1:].strip()
            if content and content not in line_map:
                line_map[content]=current_line
        elif line.startswith("-"):
            continue
        else:
            current_line+=1
    return line_map
def assign_line_numbers(diff:str,findings:list):
    line_map=build_line_map(diff)
    for finding in findings:
        content=finding.line_content.strip()
        if content in line_map:
            finding.line=line_map[content]
    return findings