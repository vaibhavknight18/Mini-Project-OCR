from sympy import symbols, Eq, solve, sympify, sqrt
import unicodedata
import re

def normalize_equation(equation_str):
    """Normalize styled unicode characters like full-width fonts etc."""
    return unicodedata.normalize('NFKC', equation_str)

def insert_implicit_multiplication(equation_str):
    """
    Insert '*' between:
    - numbers and variables: 3y → 3*y
    - variables next to variables: xy → x*y
    - numbers/variables and parentheses: 2(x+1) or x(x+1) → 2*(x+1), x*(x+1)
    """
    # 3y → 3*y
    equation_str = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', equation_str)
    # xy → x*y
    equation_str = re.sub(r'([a-zA-Z])([a-zA-Z])', r'\1*\2', equation_str)
    # x( → x*(
    equation_str = re.sub(r'([a-zA-Z0-9])(\()', r'\1*\2', equation_str)
    # )x → )*x
    equation_str = re.sub(r'(\))([a-zA-Z0-9])', r'\1*\2', equation_str)
    return equation_str

def solve_equation(equation_str):
    """Solve linear/quadratic equations with implicit multiplication support."""
    try:
        # Step 1: Normalize characters
        equation_str = normalize_equation(equation_str)
        print(f"Raw Input: {equation_str}")

        # Step 2: Basic cleanup
        if '=' not in equation_str:
            raise ValueError("Equation must contain '='")

        left_side, right_side = equation_str.split('=')
        left_side = left_side.strip().replace('^', '**').replace('−', '-').replace('÷', '/')
        right_side = right_side.strip().replace('^', '**').replace('−', '-').replace('÷', '/')

        # Step 3: Insert implicit multiplications
        left_side = insert_implicit_multiplication(left_side)
        right_side = insert_implicit_multiplication(right_side)

        print(f"Processed Equation: {left_side} = {right_side}")

        # Step 4: Detect variable (x or y)
        equation_lower = (left_side + right_side).lower()
        variable = 'x' if 'x' in equation_lower else 'y'
        var = symbols(variable)

        # Step 5: Convert to SymPy expressions
        left_expr = sympify(left_side, locals={variable: var})
        right_expr = sympify(right_side, locals={variable: var})
        eq = Eq(left_expr, right_expr)

        # Step 6: Check if it's a quadratic equation
        poly_expr = (left_expr - right_expr)
        poly = poly_expr.as_poly(var)

        if poly is not None and poly.degree() == 2:
            # Quadratic case
            a, b, c = poly.all_coeffs()
            discriminant = b**2 - 4*a*c
            print(f"Quadratic Detected: a={a}, b={b}, c={c}, Discriminant={discriminant}")

            if discriminant > 0:
                root1 = (-b + sqrt(discriminant)) / (2*a)
                root2 = (-b - sqrt(discriminant)) / (2*a)
                result = f"Quadratic equation detected. Two real roots: {root1}, {root2}"
            elif discriminant == 0:
                root = -b / (2*a)
                result = f"Quadratic equation detected. One real root: {root}"
            else:
                root1 = (-b + sqrt(discriminant)) / (2*a)
                root2 = (-b - sqrt(discriminant)) / (2*a)
                result = f"Quadratic equation detected. Complex roots: {root1}, {root2}"
        else:
            # Linear/general solver
            solution = solve(eq, var)
            result = str(solution) if solution else "No solution found"

        print(f"Solution: {result}")
        return result

    except Exception as e:
        error_msg = f"Error solving equation: {str(e)}"
        print(error_msg)
        return error_msg
