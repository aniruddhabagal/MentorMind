from langchain_core.tools import tool

@tool
def explain_science_concept(concept: str, student_grade_level: int) -> str:
    """
    Tool to explain scientific concepts at the appropriate grade level.
    
    Args:
        concept (str): The scientific concept to explain
        student_grade_level (int): The student's grade level (1-12)
    
    Returns:
        str: Age-appropriate explanation with examples
    """
    # Implementation would adapt explanations based on grade level
    return f"Here's how '{concept}' works, explained for grade {student_grade_level}: [explanation with examples]"