from unittest import TestCase
from main import LexemeAnalyzer, PostfixCalculator


class CalculateTest(TestCase):
    def __init__(self, *args, **kwargs):
        super(CalculateTest, self).__init__(*args, **kwargs)
        self.calculator = PostfixCalculator()
        self.analyzer = LexemeAnalyzer()

    def test_plus(self):
        equation = "1+1"
        postfix = self.analyzer.lex(equation)
        result = self.calculator.calculate_postfix(postfix)
        self.assertEqual(result, eval(equation))

    def test_minus(self):
        equation = '30-1'
        postfix = self.analyzer.lex(equation)
        result = self.calculator.calculate_postfix(postfix)
        self.assertEqual(result, eval(equation))

    def test_multiple(self):
        equation = '30*3'
        postfix = self.analyzer.lex(equation)
        result = self.calculator.calculate_postfix(postfix)
        self.assertEqual(result, eval(equation))

    def test_divide(self):
        equation = '20/23'
        postfix = self.analyzer.lex(equation)
        result = self.calculator.calculate_postfix(postfix)
        self.assertEqual(result, eval(equation))

    def test_bracket(self):
        equation = '(2+3)+2+4/2+(1+2)'
        postfix = self.analyzer.lex(equation)
        result = self.calculator.calculate_postfix(postfix)
        self.assertEqual(result, eval(equation))

    def test_negative_number(self):
        equation = "(-3+5)*2-1"
        postfix = self.analyzer.lex(equation)
        result = self.calculator.calculate_postfix(postfix)
        self.assertEqual(result, eval(equation))

    def test_multiple_bracket(self):
        equation = "(((-2 + 5) * 2 + 1) /2 -1 * (5 -3)) + 2"
        postfix = self.analyzer.lex(equation)
        result = self.calculator.calculate_postfix(postfix)
        self.assertEqual(result, eval(equation))

    def test_decimal_point(self):
        equation = "2.44+1+3+3+(2+1)"
        postfix = self.analyzer.lex(equation)
        result = self.calculator.calculate_postfix(postfix)
        self.assertEqual(result, eval(equation))

    def test_valid_syntax(self):
        equation = "(1 + 2"
        self.assertRaises(Exception, lambda: self.analyzer.check_expreesion(equation))

        equation = "1 + +"
        self.assertRaises(Exception, lambda: self.analyzer.check_expreesion(equation))

        equation = "1  2"
        self.assertRaises(Exception, lambda: self.analyzer.check_expreesion(equation))
