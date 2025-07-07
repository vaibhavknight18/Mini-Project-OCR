# solve_equation_file.py
from sympy import symbols, Eq, solve, sympify

def solve_equation(equation_str):
    """Solve a mathematical equation using sympy."""
    try:
        # Log input for debugging
        print(f"Input equation: {equation_str}")

        # Ensure equation contains '='
        if '=' not in equation_str:
            raise ValueError("Equation must contain '='")

        # Split into left and right sides
        left_side, right_side = equation_str.split('=')
        left_side = left_side.strip()
        right_side = right_side.strip()

        # Detect variable (x or y)
        equation_lower = equation_str.lower()
        variable = 'x' if 'x' in equation_lower else 'y'
        var = symbols(variable)

        # Preprocess to handle OCR issues
        left_side = left_side.replace('^', '**').replace(' ', '').replace('−', '-').replace('÷', '/')
        right_side = right_side.replace('^', '**').replace(' ', '').replace('−', '-').replace('÷', '/')
        # Handle implicit multiplication (e.g., "3y" -> "3*y")
        if variable in left_side:
            left_side = left_side.replace(variable, f'*{variable}')
            left_side = left_side.replace(f'*{variable}**', f'{variable}**')  # Fix power terms
        if variable in right_side:
            right_side = right_side.replace(variable, f'*{variable}')
            right_side = right_side.replace(f'*{variable}**', f'{variable}**')
        # Handle superscripts (e.g., "y2" -> "y**2")
        left_side = left_side.replace(f'{variable}2', f'{variable}**2')
        right_side = right_side.replace(f'{variable}2', f'{variable}**2')

        print(f"Preprocessed left: {left_side}, right: {right_side}")  # Debug

        # Parse expressions with sympify
        left_expr = sympify(left_side, locals={variable: var})
        right_expr = sympify(right_side, locals={variable: var})

        # Create and solve equation
        eq = Eq(left_expr, right_expr)
        solution = solve(eq, var)

        # Convert solution to string
        result = str(solution) if solution else "No solution found"
        print(f"Solution: {result}")  # Debug
        return result

    except Exception as e:
        error_msg = f"Error solving equation: {str(e)}"
        print(error_msg)  # Debug
        return error_msg