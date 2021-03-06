# pylint: disable=too-few-public-methods, no-absolute-import,missing-docstring
"""Test function argument checker"""

def decorator(fun):
    """Decorator"""
    return fun


class DemoClass(object):
    """Test class for method invocations."""

    @staticmethod
    def static_method(arg):
        """static method."""
        return arg + arg

    @classmethod
    def class_method(cls, arg):
        """class method"""
        return arg + arg

    def method(self, arg):
        """method."""
        return (self, arg)

    @decorator
    def decorated_method(self, arg):
        """decorated method."""
        return (self, arg)


def function_1_arg(first_argument):
    """one argument function"""
    return first_argument

def function_3_args(first_argument, second_argument, third_argument):
    """three arguments function"""
    return first_argument, second_argument, third_argument

def function_default_arg(one=1, two=2):
    """fonction with default value"""
    return two, one


function_1_arg(420)
function_1_arg()  # [no-value-for-parameter]
function_1_arg(1337, 347)  # [too-many-function-args]

function_3_args(420, 789)  # [no-value-for-parameter]
# +1:[no-value-for-parameter,no-value-for-parameter,no-value-for-parameter]
function_3_args()
function_3_args(1337, 347, 456)
function_3_args('bab', 'bebe', None, 5.6)  # [too-many-function-args]

function_default_arg(1, two=5)
function_default_arg(two=5)

function_1_arg(bob=4)  # [unexpected-keyword-arg,no-value-for-parameter]
function_default_arg(1, 4, coin="hello")  # [unexpected-keyword-arg]

function_default_arg(1, one=5)  # [redundant-keyword-arg]

# Remaining tests are for coverage of correct names in messages.
LAMBDA = lambda arg: 1

LAMBDA()  # [no-value-for-parameter]

def method_tests():
    """Method invocations."""
    demo = DemoClass()
    demo.static_method()  # [no-value-for-parameter]
    DemoClass.static_method()  # [no-value-for-parameter]

    demo.class_method()  # [no-value-for-parameter]
    DemoClass.class_method()  # [no-value-for-parameter]

    demo.method()  # [no-value-for-parameter]
    DemoClass.method(demo)  # [no-value-for-parameter]

    demo.decorated_method()  # [no-value-for-parameter]
    DemoClass.decorated_method(demo)  # [no-value-for-parameter]

# Test a regression (issue #234)
import sys

class Text(object):
    """ Regression """

    if sys.version_info > (3,):
        def __new__(cls):
            """ empty """
            return object.__new__(cls)
    else:
        def __new__(cls):
            """ empty """
            return object.__new__(cls)

Text()

class TestStaticMethod(object):

    @staticmethod
    def test(first, second=None, **kwargs):
        return first, second, kwargs

    def func(self):
        self.test(42)
        self.test(42, second=34)
        self.test(42, 42)
        self.test() # [no-value-for-parameter]
        self.test(42, 42, 42) # [too-many-function-args]


class TypeCheckConstructor(object):
    def __init__(self, first, second):
        self.first = first
        self.second = second
    def test(self):
        type(self)(1, 2, 3) # [too-many-function-args]
        # +1: [no-value-for-parameter,no-value-for-parameter]
        type(self)()
        type(self)(1, lala=2) # [no-value-for-parameter,unexpected-keyword-arg]
        type(self)(1, 2)
        type(self)(first=1, second=2)


class Test(object):
    """ lambda needs Test instance as first argument """
    lam = lambda self, icon: (self, icon)

    def test(self):
        self.lam(42)
        self.lam() # [no-value-for-parameter]
        self.lam(1, 2, 3) # [too-many-function-args]

Test().lam() # [no-value-for-parameter]
