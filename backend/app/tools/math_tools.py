from langchain_core.tools import tool
from typing import Dict, Any

@tool
def solve_math_problem(problem: str, student_grade_level: int) -> str:
    """Tool to solve math problems and explain steps at the appropriate grade level."""
    if "x²" in problem and "=" in problem:
        try:
            problem = problem.replace(" ", "").replace("=0", "")
            terms = problem.split("x²")
            a = 1  # Assuming coefficient of x² is 1
            rest = terms[1].split("x")
            b = int(rest[0].replace("+", "")) if rest[0] else 0
            c = int(rest[1].replace("+", "")) if rest[1] else 0

            for i in range(-10, 11):
                for j in range(-10, 11):
                    if i * j == c and i + j == b:
                        explanation = (
                            f"Let’s solve {problem} = 0 step-by-step for a grade {student_grade_level} student:\n\n"
                            f"1. We need two numbers that multiply to {c} and add to {b}. Those numbers are {i} and {j}.\n"
                            f"2. Rewrite the equation as (x + {i})(x + {j}) = 0.\n"
                            f"3. Set each part to zero:\n"
                            f"   - x + {i} = 0 → x = {-i}\n"
                            f"   - x + {j} = 0 → x = {-j}\n"
                            f"4. So, the solutions are x = {-i} and x = {-j}."
                        )
                        return explanation
            return f"Sorry, I couldn’t factor '{problem}' easily. For grade {student_grade_level}, try reviewing factoring techniques!"
        except Exception as e:
            return f"Error solving '{problem}': {str(e)}. Let’s try a different approach for grade {student_grade_level}."
    return f"I can’t solve '{problem}' yet for grade {student_grade_level}. Please provide a quadratic equation like 'ax² + bx + c = 0'."