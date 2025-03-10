from langchain_core.runnables import RunnableLambda
from ..activities.introduction import introduce_concept
from ..activities.practice import run_practice_session
from ..activities.assessment import assess_understanding, adaptive_learning_node
from ..activities.review import review_session
from ..tools.common_tools import create_tool_node_with_fallback

# Define node creation functions
def create_introduction_node():
    return RunnableLambda(introduce_concept)

def create_practice_node():
    return RunnableLambda(run_practice_session)

def create_assessment_node():
    return RunnableLambda(assess_understanding)

def create_adaptive_node():
    return RunnableLambda(adaptive_learning_node)

def create_review_node():
    return RunnableLambda(review_session)

def create_summary_node(generate_session_summary):
    """Create a session summary node."""
    return RunnableLambda(lambda state: {
        **state,
        "messages": state["messages"] + [("system", str(generate_session_summary(state)))]
    })