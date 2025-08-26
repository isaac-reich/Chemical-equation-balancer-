import sympy as sp
def split_equation(equation, side):
    sides = equation.split("->")
    reactants = sides[0].strip().split("+")
    products = sides[1].strip().split("+")
    elements = []

    if side == 0:
        for reactant in reactants:
            elements.append(reactant.strip())
    else:
        for product in products:
            elements.append(product.strip())

    return elements

def count_coefficients(compound):
    current_dict = {}
    stack = []
    current = ""
    number = ""
    i = 0
    while i < len(compound):
        char = compound[i]
        if char.isupper():
            symbol = char
            i += 1
            if i < len(compound) and compound[i].islower():
                symbol += compound[i]
                i +=1
            count, i = parse_number(compound, i)
            current_dict[symbol] = current_dict.get(symbol, 0) + count
        elif char == "(":
            stack.append(current_dict)
            current_dict = {}
            i += 1
        elif char == ")":
            i += 1
            multiplier, i = parse_number(compound, i)

            for elem in current_dict:
                current_dict[elem] *= multiplier

            prev_dict = stack.pop()
            for elem, count in current_dict.items():
                prev_dict[elem] = prev_dict.get(elem, 0) + count
            current_dict = prev_dict
            
        else:
            i +=1 

    return current_dict

def parse_number(s, start):
    num_str = ""
    for i in range(start, len(s)):
        if s[i].isdigit():
            num_str += s[i]
        else:
            if num_str == "":
                number = 1
            else:
                number = int(num_str)
            return number, i
    if num_str == "":
        number = 1
    else:
        number = int(num_str)
    return number, len(s)
            
    
def balance_equation(reactants, products):
    all_compounds = reactants + products
    all_elements = [element for compound in all_compounds for element in compound]


    matrix = []
    for element in all_elements:
        row = []

        for compound in reactants:
            if element in compound:
                row.append(compound[element])
            else:
                row.append(0)

        for compound in products:
            if element in compound:
                row.append(-compound[element])
            else:
                row.append(0)

        matrix.append(row)

    A = sp.Matrix(matrix)

    nullspace = A.nullspace()

    if len(nullspace) == 0:
        print("No solution found.")
        return

    solution = nullspace[0]
    lcm = sp.lcm([term.q for term in solution])
    coefficients = [int(term * lcm) for term in solution]

    # Format and display the result
    reactant_names = split_equation(user_input, 0)
    product_names = split_equation(user_input, 1)

    output = ""

    for i in range(len(reactant_names)):
        coeff = coefficients[i]
        name = reactant_names[i]
        if coeff != 1:
            output += str(coeff)
        output += name
        if i != len(reactant_names) - 1:
            output += " + "
        else:
            output += " -> "

    for i in range(len(product_names)):
        coeff = coefficients[len(reactant_names) + i]
        name = product_names[i]
        if coeff != 1:
            output += str(coeff)
        output += name
        if i != len(product_names) - 1:
            output += " + "

    print("Balanced Equation:")
    print(output)

def input_equation():
    global user_input
    user_input = input("Input the equation: ")

    reactant_names = split_equation(user_input, 0)
    product_names = split_equation(user_input, 1)

    reactant_counts = []
    product_counts = []

    for name in reactant_names:
        reactant_counts.append(count_coefficients(name))

    for name in product_names:
        product_counts.append(count_coefficients(name))

    balance_equation(reactant_counts, product_counts)
    input_equation()

input_equation()
