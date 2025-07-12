from sympy import symbols, Eq, solve, sympify, sqrt
import unicodedata

def normalize_equation(equation_str):
    """Normalize equation to handle styled input characters."""
    return unicodedata.normalize('NFKD', equation_str)

def solve_equation(equation_str):
    """Solve a mathematical equation including linear and quadratic equations."""
    try:
        equation_str = normalize_equation(equation_str)
        print(f"Input equation: {equation_str}")

        if '=' not in equation_str:
            raise ValueError("Equation must contain '='")

        left_side, right_side = equation_str.split('=')
        left_side = left_side.strip().replace('^', '**').replace('−', '-').replace('÷', '/')
        right_side = right_side.strip().replace('^', '**').replace('−', '-').replace('÷', '/')

        # Detect variable
        equation_lower = equation_str.lower()
        variable = 'x' if 'x' in equation_lower else 'y'
        var = symbols(variable)

        # Use sympy to parse
        left_expr = sympify(left_side, locals={variable: var})
        right_expr = sympify(right_side, locals={variable: var})
        eq = Eq(left_expr, right_expr)

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
            # Fallback to general solver
            solution = solve(eq, var)
            result = str(solution) if solution else "No solution found"

        print(f"Solution: {result}")
        return result

    except Exception as e:
        error_msg = f"Error solving equation: {str(e)}"
        print(error_msg)
        return error_msg
