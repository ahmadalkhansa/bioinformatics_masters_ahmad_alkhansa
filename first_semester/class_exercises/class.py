def roots_of_equation(a, b, c):
    '''Input: the three parameters a, b, c; Output: the roots
       of a 2nd degree equation'''
   
    from math import sqrt

    a = float(a)
    b = float(b)
    c = float(c)

    root1 = - b - sqrt(b**2 - 4*a*c)/2*a
    root2 = - b + sqrt(b**2 - 4*a*c)/2*a

    return float(root1), float(root2)

def test_roots_of_equation():
    '''This function is meant to test the functioning of another function
       i.e., roots_of_equation(). Input is not required, Output: a string

       to be printed'''

    a = input("type the first parameter of a 2nd degree equation: ")
    b = input("type the second parameter of a 2nd degree equation: ")
    c = input("type the third parameter of a 2nd degree equation: ")

    roots = roots_of_equation(a, b, c)

    return "x0 = {0:3.1f}, x1 = {1:3.1f}".format(roots[0],roots[1])

print(test_roots_of_equation())


