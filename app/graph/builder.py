from langgraph.graph import StateGraph,START,END
from app.graph.state import ReviewState
from app.graph.nodes import (
    security_reviewer,
    performance_reviewer,
    correctness_reviewer,
    style_reviewer,
    test_coverage_reviewer,
    merge_node
)
builder=StateGraph(ReviewState)
builder.add_node("security", security_reviewer)
builder.add_node("performance", performance_reviewer)
builder.add_node("correctness", correctness_reviewer)
builder.add_node("style", style_reviewer)
builder.add_node("test_coverage", test_coverage_reviewer)
builder.add_node("merge", merge_node)
builder.add_edge(START, "security")
builder.add_edge(START, "performance")
builder.add_edge(START, "correctness")
builder.add_edge(START, "style")
builder.add_edge(START, "test_coverage")
builder.add_edge("security", "merge")
builder.add_edge("performance", "merge")
builder.add_edge("correctness", "merge")
builder.add_edge("style", "merge")
builder.add_edge("test_coverage", "merge")
builder.add_edge("merge", END)
graph = builder.compile()