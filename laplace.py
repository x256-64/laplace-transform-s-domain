import sympy 
from re import findall

def get_equation() -> str:
    print("Correct Syntax: \n- Must have constant coefficients\n- Separate terms and signs separating terms with a space after the previous term\n- Homogeneous only")
    print("Equation Syntax Example: y'' + 4y' + y = 0")
    while True: #For Input validation that will be used later
        equation:str = input("Enter a differential equation\n> ")
        break
    return equation

def parse_equation(equ:str):
    t, s = sympy.symbols('t s')
    y_cap = sympy.Function('Y')(s)
    y = sympy.Function('y')(t)

    equ_list = equ.split(" ")#If + or - is at position 0, 
    term_list_left:list[str] = []
    term_list_right:list[str] = []
    try:
        rh_index:int = equ_list.index('=')
        print(equ_list[rh_index+1])
        if(len(equ_list)!=rh_index+2 or equ_list[rh_index+1]!="0"):
            print("Homogeneous ODEs only for now")
            exit()
    except ValueError:
        print("Your equation is missing the = sign and the right hand")
        exit()
    for ind, eq in enumerate(equ_list):
        if ind%2==0:
            if (y_ind:=eq.find("y"))>-1:
                if eq[:y_ind]!="":
                    coeff = int(eq[:y_ind])
                    order:int = len(findall("'", eq))
                    term_list_left.append(coeff*y.diff(t,order))
            else:
                order:int = len(findall("'", eq))
                term_list_left.append(y.diff(t,order))


    returnable = sympy.Eq(term_list_left[0], 0)
    for ind, symbol in enumerate(equ_list):
        if ind%2!=0:
            if ind<rh_index:
                if symbol=="+":
                    returnable = sympy.Eq(returnable.lhs + sympy.Eq(term_list_left[int(ind/2)], 0).lhs, returnable.rhs)
                elif symbol=="-":
                    returnable = sympy.Eq(returnable.lhs - sympy.Eq(term_list_left[int(ind/2)], 0).lhs, returnable.rhs)
            elif ind>rh_index:
                if symbol=="+":
                    returnable = sympy.Eq(returnable.lhs, returnable.rhs)
                elif symbol=="-":
                    returnable = sympy.Eq(returnable.lhs, returnable.rhs)
    return returnable

def solve_equation() -> str:
    t, s = sympy.symbols('t s')
    y_cap = sympy.Function('Y')(s)
    y = sympy.Function('y')(t)

    eq = get_equation()
    ode = parse_equation(eq)

    lhs_laplace = sympy.laplace_transform(ode.lhs, t, s)[0]
    rhs_laplace = sympy.laplace_transform(ode.rhs, t, s)[0]

    laplace_ode = sympy.Eq(lhs_laplace, rhs_laplace)

    Y0 = 1
    Y1 = 0
    laplace_ode = laplace_ode.subs({sympy.laplace_transform(y, t, s)[0]: y_cap, y.subs(t, 0): Y0, y.diff(t).subs(t, 0): Y1})

    solution = sympy.solve(laplace_ode, y_cap)
    print(f"Solution: Y(s) = {solution[0]}")

def main():
    solve_equation()

if __name__=="__main__":
    main()
