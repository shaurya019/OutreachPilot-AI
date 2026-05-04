from langgraph.graph import END, START, StateGraph

from app.agents.state import ResearchState

from app.agents.nodes.supervisor_node import supervisor_node
from app.agents.nodes.website_research_node import website_research_node
from app.agents.nodes.company_research_node import company_research_node
from app.agents.nodes.employee_research_node import employee_research_node
from app.agents.nodes.merge_research_node import merge_research_node
from app.agents.nodes.personalization_node import personalization_node
from app.agents.nodes.report_generator_node import report_generator_node
from app.agents.nodes.email_draft_node import email_draft_node
from app.agents.nodes.reviewer_node import reviewer_node

def build_research_graph():
    builder = StateGraph(ResearchState)
    
    builder.add_node("supervisor", supervisor_node)

    builder.add_node("website_research", website_research_node)
    builder.add_node("company_research", company_research_node)
    builder.add_node("employee_research", employee_research_node)

    builder.add_node("merge_research", merge_research_node)
    builder.add_node("personalization", personalization_node)
    builder.add_node("report_generator", report_generator_node)
    builder.add_node("email_draft", email_draft_node)
    builder.add_node("reviewer", reviewer_node)

    builder.add_edge(START, "supervisor")
    
    builder.add_edge("supervisor", "website_research")
    builder.add_edge("supervisor", "company_research")
    builder.add_edge("supervisor", "employee_research")
    
    builder.add_edge("website_research", "merge_research")
    builder.add_edge("company_research", "merge_research")
    builder.add_edge("employee_research", "merge_research")

    builder.add_edge("merge_research", "personalization")
    builder.add_edge("personalization", "report_generator")
    builder.add_edge("report_generator", "email_draft")
    builder.add_edge("email_draft", "reviewer")
    builder.add_edge("reviewer", END)

    return builder.compile()

research_graph = build_research_graph()

def run_research_graph(initial_state: ResearchState) -> ResearchState:
    return research_graph.invoke(initial_state)