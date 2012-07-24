#-------------------------------------------------------------------------------
# Name:        cryptarithmetic
# 
# Author:      mourad mourafiq
#
# Copyright:   (c) mourad mourafiq
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import string, re, itertools
import time

examples = """TWO + TWO == FOUR
            A**2 + B**2 == C**2
            A**2 + BE**2 == BY**2
            A**2 + BY**2 == BE**2
            X / X == X
            X / X == 1
            A**N + B**N == C**N and N > 1
            ATOM**0.5 == A + TO + M
            GLITTER is not GOLD
            ONE < TWO and FOUR < FIVE
            ONE < TWO < THREE
            RAMN == R**3+ RM**3 == N**3 + RX**3
            sum(range(AA)) == BB
            sum(range(POP)) == BOBO
            ODD + ODD == EVEN
            PLUTO is not set([PLANETS]) """.splitlines()

def solve(formula, verbose=False):
    """Given a formula like 'ODD + ODD == EVEN', fill in digits to solve it.
    Input formula is a string; output is a digit-filled-in string or None."""
    for f in fill_in(formula):
        if valid(f):
            if not verbose: print f
            return f
    
def fill_in(formula):
    "Generate all possible fillings-in of letters in formula with digits."
    letters = ''.join(set(re.findall('[A-Z]', formula)))
    for digits in itertools.permutations('1234567890', len(letters)):
        table = string.maketrans(letters, ''.join(digits))
        yield formula.translate(table)
    
def valid(f):
    """Formula f is valid if and only if it has no 
    numbers with leading zero, and evals true."""
    try: 
        return not re.search(r'\b0[0-9]', f) and eval(f) is True
    except ArithmeticError:
        return False
    
def timedcall(fct, formula):
    """
    Calculate time of execution 
    """
    t0 = time.clock()
    fct(formula)
    t1 = time.clock()    
    return t1 - t0

def compile_formula(formula, verbose=False):
    """Compile formula into a function. Also return letters found, as a str,
    in same order as parms of function. The first digit of a multi-digit 
    number can't be 0. So if YOU is a word in the formula, and the function
    is called with Y eqal to 0, the function should return False."""
    
    first_letters = set(re.findall(r'\b([A-Z])[A-Z]', formula))        
    letters = ''.join(set(re.findall('[A-Z]', formula)))
    parms = ', '.join(letters)
    tokens = map(compile_word, re.split('([A-Z]+)', formula))
    body = ''.join(tokens)
    if first_letters:
        tests = ' and '.join(L+'!=0' for L in first_letters)
        body = '%s and (%s)' % (tests, body)
    f = 'lambda %s: %s' % (parms, body)
    if verbose: print f
    return eval(f), letters

def compile_word(word):
    """Compile a word of uppercase letters as numeric digits.
    E.g., compile_word('YOU') => '(1*U+10*O+100*Y)'
    Non-uppercase words uncahanged: compile_word('+') => '+'"""
    if word.isupper():
        terms = [('%s*%s' % (10**i, d)) 
                 for (i, d) in enumerate(word[::-1])]
        return '(' + '+'.join(terms) + ')'
    else:
        return word
    
def faster_solve(formula):
    """Given a formula like 'ODD + ODD == EVEN', fill in digits to solve it.
    Input formula is a string; output is a digit-filled-in string or None.
    This version precompilesdef k(): the formula; only one eval per formula."""
    f, letters = compile_formula(formula)
    for digits in itertools.permutations((1,2,3,4,5,6,7,8,9,0), len(letters)):
        try:
            if f(*digits) is True:
                table = string.maketrans(letters, ''.join(map(str, digits)))
                return formula.translate(table)
        except ArithmeticError:
            pass

def test1():
    t0 = time.clock()
    for example in examples:
        print '%6.4f sec : %s' % (timedcall(faster_solve, example), example)
    print '%6.4f sec in total.' % (time.clock() - t0)

def test2():
    assert faster_solve('A + B == BA') == None # should NOT return '1 + 0 == 01'
    assert faster_solve('YOU == ME**2') == ('289 == 17**2' or '576 == 24**2' or '841 == 29**2')
    assert faster_solve('X / X == X') == '1 / 1 == 1'
    return 'tests pass'
